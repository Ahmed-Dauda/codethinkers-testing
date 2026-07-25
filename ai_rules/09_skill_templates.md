# Skill Templates — Pre-Built Workflows

⚠️ **CHECK THIS FIRST.** This file does NOT redefine app classification —
see `02_application_classification.md` for the single source of truth
on Pattern 1 (Private) / Pattern 2 (Public Blog) / Pattern 3 (Public
SaaS). This file only maps each Pattern to a concrete generation
checklist, and adds the Education UI overlay.

---

## Skill: Pattern 1 — Private Staff Record System

**Classify using `02_application_classification.md` Pattern 1.**

**Generate:**
- ✅ base.html with Footer 1 + Navbar 1 (see `10_ui_patterns.md`)
- ✅ Django Admin — full CRUD for all models
- ✅ Dashboard home page with statistics (record counts, breakdowns,
  recent activity), extending base.html, using Card 1A/1B
- ✅ Export actions (CSV/DOCX via ExportAdminMixin)
- ❌ No public pages
- ❌ No public CRUD
- ❌ No authentication, unless staff need individual logins

**Views:** Only HomeView (dashboard with model counts) by default. No
ListView, DetailView, etc. — admin handles everything, unless the
prompt explicitly asks for staff-facing pages beyond the admin.

---

## Skill: Pattern 2 — Public Read-Only Blog

**Classify using `02_application_classification.md` Pattern 2.**

**Generate:**
- ✅ base.html with Footer 2 + Navbar 2 (see `10_ui_patterns.md`)
- ✅ Django Admin — full CRUD
- ✅ Public pages — post list (with pagination), post detail, using
  Card 2A/2B for previews/categories
- ✅ Views — ListView, DetailView only
- ❌ No Create/Update/Delete for public
- ❌ No authentication, unless comments require login

---

## Skill: Pattern 3 — Public Full CRUD / SaaS

**Classify using `02_application_classification.md` Pattern 3.**

**Generate:**
- ✅ base.html with Footer 3 + Navbar 3 (see `10_ui_patterns.md`)
- ✅ Django Admin — full CRUD
- ✅ Public pages — list, detail, create, update, delete, using Card
  3A/3B for features/pricing
- ✅ All 5 views per model, scoped to `self.request.user`
- ✅ Forms with validation
- ✅ Full authentication: login, logout, signup

---

## UI Overlay: Education / School / LMS

**Trigger words:** school, student, bootcamp, course, class (as in
"class schedule" — NOT a Python/CSS `class`), academy, grade (as in
academic grade — NOT `list_grade` or similar field names), campus, LMS.

⚠️ This is a UI overlay, not a fourth classification pattern. Education
trigger words tell you WHICH FOOTER/NAVBAR/CARD SET to use — they do
NOT override the Pattern decision from `02_application_classification.md`.
Classify the Pattern first using the Decision Checklist there, THEN
apply this overlay if education trigger words are present.

**How to combine:**
1. Run the Pattern 1/2/3 classification as normal (does the user own
   private data and log in? → Pattern 3. Read-only public content? →
   Pattern 2. Staff/admin only, nobody logs in? → Pattern 1.)
2. If education trigger words are present, swap the UI set from that
   Pattern's default (Footer/Navbar/Card 1, 2, or 3) to **Footer/Navbar/
   Card 4** from `10_ui_patterns.md`.
3. Everything else (views, auth, models) still follows the underlying
   Pattern's checklist above — Education only changes the visual layer.

**Example:** "Students log in to see their courses and grades" → each
student owns private data and authenticates → **Pattern 3** rules apply
(full auth, user-scoped views, all 5 views where appropriate) → but use
**Footer 4 / Navbar 4 / Card 4** instead of Footer/Navbar/Card 3, because
education trigger words are present.

**Example:** "Internal system for teachers to record student attendance"
→ only staff use it, no public/student logins → **Pattern 1** rules
apply (admin-only, dashboard home page) → use **Footer 4 / Navbar 4 /
Card 4** instead of Footer/Navbar/Card 1.

---

## Default: When Nothing Matches

If the user's request doesn't clearly match a Pattern:
1. Is this private (admin-only) or public? Re-check the Decision
   Checklist in `02_application_classification.md`.
2. What pages did the user explicitly ask for?
3. Default to Pattern 1 (Private) if unsure — safer to not generate
   public pages than to generate unwanted ones.
4. Default to the base Footer/Navbar/Card set (1/2/3) if no education
   trigger words are present — don't apply the Education overlay
   speculatively.