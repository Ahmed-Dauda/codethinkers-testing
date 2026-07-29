# Common Fixes — Used When a Previous Build Attempt Failed

⚠️ IMPORTANT: Respect the original app type. If the first attempt correctly identified this as a PRIVATE app (no public views, only HomeView + Admin), do NOT add public CRUD views in your fix. Only fix the specific validation errors listed — don't add new features or change the app type.

When you're told your previous response failed validation, apply these
fixes based on the specific error category shown:

1. If 'missing template_name': Add `template_name = 'xxx.html'` as the
   FIRST line in every CBV class.
2. If 'no view in views.py': Create only the views the request actually
   needs — don't invent extras.
3. If 'no matching URL pattern': Add path() entries using EXACT names:
   `{model}_list`, `{model}_detail`, `{model}_create`, `{model}_update`,
   `{model}_delete`.
4. If 'uses self.request.user but doesn't inherit LoginRequiredMixin':
   do ONE of these:
   a) Add LoginRequiredMixin to the class AND create registration/login.html
      AND add accounts/ URLs, OR
   b) Remove self.request.user from the view and don't require login
      (simpler — do this if the user didn't ask for auth).
5. If 'uses LoginRequiredMixin/@login_required but no login template
   exists (registration/login.html)' or 'TemplateDoesNotExist:
   registration/login.html': do ONE of these:
   a) Create registration/login.html (a real login form template) AND
      add `path('accounts/', include('django.contrib.auth.urls'))` to
      root urls.py AND set `LOGIN_REDIRECT_URL` in settings.py, OR
   b) Remove LoginRequiredMixin/@login_required from the view entirely
      and don't require login (simpler — do this if the user didn't
      explicitly ask for user accounts/self-service signup).
   Do NOT leave LoginRequiredMixin in place without doing (a) — that
   combination crashes with TemplateDoesNotExist on the very first
   unauthenticated request.
6. Every `{% url %}` tag MUST use namespace: `{% url 'app_name:name' %}`.
7. If 'list_select_related': Add `list_select_related = ('fk_field',)` to
   EVERY ModelAdmin.
8. If 'shows ForeignKey field(s)': Add the EXACT list_select_related tuple
   shown in the error message.
9. If 'references missing template': Ensure templates extend base.html and
   select a footer per your Footer Selection Rules.
10. If 'Model 'X' used but not imported': X is being referenced in
    views.py/urls.py/admin.py but was never defined as a class in
    models.py. Add the missing `class X(models.Model): ...` definition
    with real fields — do not just fix the import statement, the model
    itself is missing.

Do NOT just change self_check to PASS — actually add the missing code.

# Common Fixes — Auto-Applied Failure Patterns

When the AI's output fails static validation or smoke tests, match the error
to one of these patterns and include the corresponding fix instruction in the
retry prompt. Each pattern below represents a bug class that has been
permanently solved — add new ones every time a novel failure reaches production.

---

## FIX-001: Missing ExportAdminMixin
**Symptom:** `admin.py is missing the ExportAdminMixin class`
**Cause:** AI generated @admin.register() without the required ExportAdminMixin
**Fix instruction for AI retry:**
"Your admin.py MUST include the ExportAdminMixin class at the top (before any
ModelAdmin class) and every ModelAdmin MUST inherit from it:
`class FooAdmin(ExportAdminMixin, admin.ModelAdmin)`"

---

## FIX-002: LoginRequiredMixin Missing
**Symptom:** `uses self.request.user but doesn't inherit LoginRequiredMixin`
**Cause:** View filters by user but doesn't block anonymous visitors
**Fix instruction for AI retry:**
"Every view that accesses self.request.user MUST inherit LoginRequiredMixin.
Add `from django.contrib.auth.mixins import LoginRequiredMixin` and change
`class FooView(ListView):` to `class FooView(LoginRequiredMixin, ListView):`"

---

## FIX-003: Missing Login Template
**Symptom:** `no login template exists (registration/login.html)`
**Cause:** LoginRequiredMixin used but no login template provided
**Fix instruction for AI retry:**
"Include a registration/login.html template that extends base.html with a
standard Django login form (csrf_token, form.as_p, submit button)."

---

## FIX-004: F()/Q()/Count() Without Import
**Symptom:** `uses 'models.F()/Q()/Count()' but is missing 'from django.db import models'`
**Cause:** views.py uses models.F() but only imported models from .models, not django.db
**Fix instruction for AI retry:**
"Add `from django.db import models` at the top of views.py when using
models.F(), models.Q(), models.Count(), or similar expressions."

---

## FIX-005: App Not in INSTALLED_APPS
**Symptom:** `App 'X' not registered in INSTALLED_APPS`
**Cause:** models.py created but app not added to settings
**Fix instruction for AI retry:**
"Make sure the app name is included in INSTALLED_APPS in settings.py."

---

## FIX-006: Model Not Registered in Admin
**Symptom:** `Model 'X' isn't registered in admin.py`
**Cause:** Model exists but has no @admin.register() decorator
**Fix instruction for AI retry:**
"Every model MUST have an @admin.register() with ExportAdminMixin,
list_display (3-5 fields), list_filter, search_fields, and list_per_page=25."

---

## FIX-007: Template Name Missing on CBV
**Symptom:** `is missing template_name`
**Cause:** Class-based view doesn't set template_name explicitly
**Fix instruction for AI retry:**
"Every class-based view (ListView, DetailView, CreateView, etc.) MUST set
template_name explicitly. Never rely on Django's default template name inference."

---

## FIX-008: URL Name Not Found
**Symptom:** `calls {% url 'X' %} — undefined name`
**Cause:** Template references a URL name that doesn't exist in urls.py
**Fix instruction for AI retry:**
"Every {% url 'X' %} in templates MUST match a name='X' in urls.py.
Use namespaced URLs: {% url 'app_name:view_name' %}."

---

## FIX-009: View Referenced But Not Defined
**Symptom:** `references views.X, not found in views.py`
**Cause:** urls.py references a view class/function that doesn't exist
**Fix instruction for AI retry:**
"Every views.X referenced in urls.py MUST exist as a class or function in views.py."

---

## FIX-010: list_select_related Missing
**Symptom:** `shows ForeignKey field(s) in list_display/list_filter without list_select_related`
**Cause:** Admin shows FK fields but doesn't use select_related — N+1 query risk
**Fix instruction for AI retry:**
"Add list_select_related listing every ForeignKey field that appears in
list_display or list_filter. Also add a get_queryset method with matching
select_related calls."

---

## FIX-011: Truncated File Content
**Symptom:** `new content (N chars) looks truncated vs original (M chars)`
**Cause:** AI response was cut off mid-file
**Fix instruction for AI retry:**
"Your previous response was truncated. Generate fewer, more focused files.
Prioritize models.py, views.py, urls.py, admin.py, and 2-3 key templates.
Skip verbose comments and unnecessary template variations."

---

## FIX-012: Syntax Error in Generated Python
**Symptom:** `line N: invalid syntax` or `SyntaxError`
**Cause:** AI generated invalid Python (f-string quote collision, missing colon, etc.)
**Fix instruction for AI retry:**
"Your generated Python code has a syntax error. Double-check all f-strings
use consistent quotes (if the string contains double quotes, wrap in single
quotes), all class/function definitions have colons, and all brackets are
properly closed."

---

## How to add a new fix:
1. When a novel failure reaches production, add it here with a unique FIX-XXX number
2. Include: symptom (copy-paste the exact error message), cause, and fix instruction
3. The retry logic will automatically include this file in the AI's context