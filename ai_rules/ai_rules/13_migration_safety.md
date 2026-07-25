# Migration Safety

Your model changes get converted into real Django migrations that run
against a live database with existing data. Follow these rules so
migrations apply cleanly without manual intervention.

## When Adding a New Model to an Existing App

- A new model (e.g. adding `StudentScore` to an app that already has
  `Question`, `Quiz`, `Answer`) must NOT require any change to existing
  models' fields unless the user's request explicitly calls for it.
- If the new model has a ForeignKey to an existing model, that's fine —
  it doesn't require altering the existing model's table.
- Do NOT add unrelated fields to existing models "for consistency" or
  "best practice" when the user only asked for a new feature. Every
  field you add or change is a real schema change against real data.

## When Modifying an Existing Model

- Adding a new field to an existing model: it MUST either have a
  `default=` value, or be `null=True`. A new required field with no
  default breaks migration on any table that already has rows.
- NEVER rename a field. Renaming is indistinguishable from
  "delete old field, add new field" to Django's migration system,
  which means real data in that column gets silently dropped. If a
  field's name is genuinely wrong, add a new field instead and leave
  the old one, or explicitly note in your analysis that this requires
  a manual data migration the user should be warned about.
- NEVER change a field's type in a way that could lose precision or
  fail to parse existing data (e.g. CharField → IntegerField). If this
  is genuinely needed, say so in your analysis rather than silently
  generating the change.
- Do NOT delete a model or field unless the user explicitly asked for
  that data/feature to be removed.

## Foreign Keys

- Every new ForeignKey field pointing at an existing model needs either
  `null=True` or `default=` (or the migration will fail if the existing
  table already has rows, since Django can't populate a required FK
  with no value on rows that already exist).
- Prefer `on_delete=models.CASCADE` unless the user's request implies
  the related object should survive deletion of its parent (then use
  `SET_NULL` with `null=True`, or `PROTECT`).

## What to Do When Unsure

If a requested change is genuinely destructive to existing data (field
removal, type change, rename), do NOT silently apply it. Instead:
1. Make the additive-safe version of the change if one exists, and
2. Note in your "analysis" field exactly what a full implementation
   would require and why you didn't do it automatically.

This keeps every migration you generate safe to apply against a
database that already has real rows in it — never assume the
database is empty.