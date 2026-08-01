# ─────────────────────────────────────────────────────────────
# Add these three functions to webprojects/views.py, ABOVE
# _apply_incremental_changes and _scaffold_build (both call them).
# Also add this import near your other imports at the top of the file:
#     from .models import BuildAttempt
# ─────────────────────────────────────────────────────────────
import re
from pathlib import Path
from django.conf import settings
from .models import BuildAttempt


def _log_build_attempt(
    project, build_type, prompt, attempt_number, outcome,
    validation_errors=None, smoke_test_errors=None,
    fix_patterns_triggered=None, rule_files_loaded=None,
    duration_seconds=None,
):
    """Record one build attempt. Call this at every terminal point of the
    apply/scaffold pipeline — both success and every failure branch —
    not just at the very end. We want a row per ATTEMPT, not per REQUEST,
    so we can see the full retry trajectory (attempt 1 failed on X,
    attempt 2 fixed X but hit Y, attempt 3 succeeded)."""
    try:
        BuildAttempt.objects.create(
            project=project,
            build_type=build_type,
            prompt=(prompt or "")[:5000],
            attempt_number=attempt_number,
            outcome=outcome,
            validation_errors=validation_errors or [],
            smoke_test_errors=smoke_test_errors or [],
            fix_patterns_triggered=fix_patterns_triggered or [],
            rule_files_loaded=rule_files_loaded or [],
            duration_seconds=duration_seconds,
        )
    except Exception as e:
        # Logging must never break the actual build — if this fails,
        # print and move on, don't let observability take down the feature.
        print(f"⚠️ _log_build_attempt failed (non-fatal): {e}")


def _extract_fix_ids_from_error_text(text):
    """Given a chunk of validation/failure text, find which FIX-XXX
    entries from 13_common_fixes.md have a matching symptom substring —
    used to tag an attempt with which known patterns it hit, even before
    _auto_fix_failure runs (so we can log 'attempt 1 hit FIX-007' even
    if auto-fix wasn't triggered or didn't apply it)."""
    fixes_path = Path(settings.BASE_DIR) / "ai_rules" / "13_common_fixes.md"
    if not fixes_path.exists() or not text:
        return []

    content = fixes_path.read_text(encoding="utf-8")
    entries = re.findall(
        r'## (FIX-\d+):.*?\n\*\*Symptom:\*\*\s*`(.*?)`', content, re.DOTALL
    )
    matched = []
    for fix_id, symptom in entries:
        if symptom.strip() and symptom.strip() in text:
            matched.append(fix_id)
    return matched


def mark_previous_attempt_fix_resolution(project, build_type):
    """Call this right after logging a SUCCESSFUL attempt. Looks back at
    the immediately preceding failed attempt for the same project+build
    type, and marks each fix_id it had flagged as 'resolved': True —
    this is the retroactive labeling that lets us later compute each
    FIX-XXX's real-world success rate."""
    try:
        recent = list(
            BuildAttempt.objects
            .filter(project=project, build_type=build_type)
            .order_by("-created_at")[:2]
        )
        if len(recent) < 2:
            return
        latest, previous = recent[0], recent[1]
        if latest.outcome.startswith("success") and previous.fix_patterns_triggered:
            updated = [
                {**entry, "resolved": True}
                for entry in previous.fix_patterns_triggered
            ]
            previous.fix_patterns_triggered = updated
            previous.save(update_fields=["fix_patterns_triggered"])
    except Exception as e:
        print(f"⚠️ mark_previous_attempt_fix_resolution failed (non-fatal): {e}")