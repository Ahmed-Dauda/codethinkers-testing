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


---
## FIX-013: Missing list_select_related for FK fields
**Symptom:** `shows ForeignKey field(s)`
**Cause:** Admin displays FK fields without select_related — causes N+1 queries
**Fix instruction for AI retry:** "Add list_select_related with the exact FK fields shown in the error message."

---

## FIX-014: ImageField not displaying images
**Symptom:** `images not displaying` or `image not showing`
**Cause:** Missing ImageField setup — no Pillow, no MEDIA config, wrong template syntax, or missing enctype
**Fix instruction for AI retry:** "For any model with image fields: 1) Use `models.ImageField(upload_to='uploads/')` with Pillow in requirements.txt. 2) In settings.py add `MEDIA_URL = '/media/'` and `MEDIA_ROOT = BASE_DIR / 'media'`. 3) In urls.py add `static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)` inside `if settings.DEBUG:`. 4) In templates use `{{ object.image.url }}` NOT `{{ object.image }}`. 5) Forms with file uploads MUST have `enctype='multipart/form-data'`. 6) Views handling file uploads must include `request.FILES` in the form constructor."
---

## FIX-001: Remove unexpected indent
**Symptom:** `unexpected indent`
**Cause:** This error occurs when there is an extra space or tab at the beginning of a line that is not expected by Python's indentation rules.
**Fix instruction for AI retry:** "Open `boutique_fashion_store/urls.py`, remove any leading spaces or tabs on line 1, and ensure it starts at the beginning of the line."

## FIX-001: Missing attribute in list_display
**Symptom:** `list_display refers to 'created_at'`
**Cause:** The 'created_at' field is not defined in the CartItem or OrderItem models.
**Fix instruction for AI retry:** "Check the CartItem and OrderItem models to ensure that the 'created_at' field is defined. If it is missing, add a DateTimeField named 'created_at' to both models. If it exists, ensure it is correctly spelled and accessible."

---

## FIX-001: Cart URL Handling
**Symptom:** `/cart/`
**Cause:** The URL pattern for the cart view is not properly defined or is missing in the URL configuration.
**Fix instruction for AI retry:** "Check the `urls.py` file to ensure that the URL pattern for the cart view is correctly defined. If missing, add a path for the cart view, e.g., `path('cart/', views.cart_view, name='cart')`."


---

## FIX-001: Category List Route Error
**Symptom:** `/category/`
**Cause:** The route for the category list is not properly defined in the URL configuration.
**Fix instruction for AI retry:** "Check the urls.py file to ensure that the path for 'category_list' is correctly defined. If missing, add a path entry like `path('category/', views.category_list, name='category_list')`."


---

## FIX-001: Checkout URL Error
**Symptom:** `/checkout/`
**Cause:** The URL pattern for the checkout view is not correctly defined in the Django URL configuration.
**Fix instruction for AI retry:** "Check the `urls.py` file for the checkout path definition. Ensure that the path for the checkout view is correctly set up, e.g., `path('checkout/', views.checkout_view, name='checkout')`. If the view function does not exist, create it in the corresponding views file."


---

## FIX-001: Home Route Error
**Symptom:** `home (/)`
**Cause:** The home route is not properly defined in the URL configuration.
**Fix instruction for AI retry:** "Check the urls.py file to ensure that the home route is defined correctly. Ensure that the view function is imported and mapped to the correct URL pattern."


---

## FIX-001: Product List View Error
**Symptom:** `product_list`
**Cause:** The view for the product list is not properly defined or is missing in the URL configuration.
**Fix instruction for AI retry:** "Check the URL patterns in your `urls.py` file to ensure that the `product_list` view is correctly mapped. If it is missing, add a path for the `product_list` view. If it exists, verify that the view function is correctly implemented and returns a valid response."


---

## FIX-001: Review List URL Issue
**Symptom:** `/review/`
**Cause:** The URL pattern for the review list view is not correctly defined in the Django URL configuration.
**Fix instruction for AI retry:** "Check the urls.py file for the correct path definition for the review list view. Ensure that the path is defined as `path('review/', ReviewListView.as_view(), name='review_list')` and that the corresponding view is properly imported."


---

## FIX-001: Remove unexpected indent
**Symptom:** `unexpected indent`
**Cause:** This error occurs when there is an extra space or tab at the beginning of a line where it is not expected.
**Fix instruction for AI retry:** "Open `boutique_fashion_store_app/models.py`, remove any leading spaces or tabs on line 1, and ensure the indentation is consistent with the rest of the file."

## FIX-001: Admin list_display attribute error
**Symptom:** `not a callable, an attribute of 'CartAdmin'`
**Cause:** The attributes 'created_at' and 'updated_at' are not defined in the Cart model or are incorrectly referenced in the CartAdmin class.
**Fix instruction for AI retry:** "Check the Cart model to ensure that 'created_at' and 'updated_at' fields are defined. If they are missing, add them as DateTimeField attributes. If they exist, ensure that they are correctly referenced in the CartAdmin's list_display attribute."

---

## FIX-001: Add list_select_related for ForeignKey fields
**Symptom:** `ForeignKey field(s) in list_display/list_filter without list_select_related`
**Cause:** This occurs when ForeignKey fields are used in the admin list display or filters without optimizing the query, leading to N+1 queries.
**Fix instruction for AI retry:** "Open boutique_fashion_store/admin.py, locate the ProductAdmin class, and add the line list_select_related = ('category',) within the class definition."


---

## FIX-001: Add list_select_related for ForeignKey fields
**Symptom:** `ForeignKey field(s) in list_display/list_filter without list_select_related`
**Cause:** This happens when ForeignKey fields are included in the admin list display or filters without using `list_select_related`, leading to N+1 query issues.
**Fix instruction for AI retry:** "In the CartAdmin class within boutique_fashion_store/admin.py, add the line `list_select_related = ('user',)` to optimize database queries."


---

## FIX-001: Optimize OrderAdmin for ForeignKey fields
**Symptom:** `ForeignKey field(s) in list_display/list_filter without list_select_related`
**Cause:** This happens because ForeignKey fields in the admin are displayed without using `list_select_related`, leading to N+1 query issues.
**Fix instruction for AI retry:** "In the `OrderAdmin` class in `boutique_fashion_store/admin.py`, add the line `list_select_related = ('cart',)` to optimize the query performance."


---

## FIX-001: Add list_select_related to ReviewAdmin
**Symptom:** `ForeignKey field(s) in list_display/list_filter without list_select_related`
**Cause:** This happens when ForeignKey fields are included in the admin list display or filters without optimizing the query, leading to N+1 queries.
**Fix instruction for AI retry:** "In boutique_fashion_store/admin.py, locate the ReviewAdmin class and add the line list_select_related = ('product', 'user') to optimize the query."


---

## FIX-001: Model Content Truncation
**Symptom:** `new content looks truncated`
**Cause:** The new content exceeds the maximum allowed character limit for the model field.
**Fix instruction for AI retry:** "Review the model field definitions in boutique_fashion_store_app/models.py and ensure that the new content does not exceed the defined character limits. Adjust the field types or increase the limits as necessary."

## FIX-001: Invalid list_display configuration
**Symptom:** `The value of 'list_display' must be a list or tuple`
**Cause:** The `list_display` attribute in the `CartAdmin` class is not defined as a list or tuple.
**Fix instruction for AI retry:** "Open the `CartAdmin` class in `admin.py`, locate the `list_display` attribute, and ensure it is defined as a list or tuple, e.g., `list_display = ('field1', 'field2')`."

---

## FIX-001: Truncated content in URL configuration
**Symptom:** `new content looks truncated`
**Cause:** The generated URL content exceeds the maximum character limit allowed for a single entry.
**Fix instruction for AI retry:** "Review the URL patterns in boutique_fashion_store/urls.py and ensure that each entry does not exceed the character limit. If necessary, split long URL patterns into multiple lines or simplify them."


---

## FIX-001: Truncated content in settings.py
**Symptom:** `new content looks truncated`
**Cause:** The content being written to settings.py exceeds the allowed character limit for the update process.
**Fix instruction for AI retry:** "Check the length of the new content being generated for settings.py. If it exceeds the limit, split the content into smaller chunks or ensure the content is correctly formatted before applying."


---

## FIX-001: Template Content Truncation
**Symptom:** `new content looks truncated`
**Cause:** The new content exceeds the character limit set for template updates.
**Fix instruction for AI retry:** "Increase the character limit for template content updates in the code generator configuration."


---

## FIX-001: Missing App URL Configuration
**Symptom:** `not wired into root urls.py`
**Cause:** The app's URLs are not included in the project's main URL configuration.
**Fix instruction for AI retry:** "Open the root `urls.py` file and add an import statement for the app's URLs. Then, include the app's URL patterns using `path()` or `include()`."


---

## FIX-001: Invalid Pattern Usage
**Symptom:** `completely fictitious pattern`
**Cause:** The code is attempting to use a pattern that is not defined or recognized by the system.
**Fix instruction for AI retry:** "Review the pattern definitions in the codebase and replace the fictitious pattern with a valid one from the existing patterns."


---

## FIX-023: [TODO: Name this error]
**Symptom:** `⚠️ boutique_fashion_store_app/templates/home.html: new content (75 chars) looks truncated vs original (1013 chars). Not`
**Cause:** [TODO: Add root cause]
**Fix instruction for AI retry:** "[TODO: Add specific fix steps]"


---

## FIX-024: [TODO: Name this error]
**Symptom:** `❌ boutique_fashion_store_app/urls.py not wired into root urls.py`
**Cause:** [TODO: Add root cause]
**Fix instruction for AI retry:** "[TODO: Add specific fix steps]"


---

## FIX-025: [TODO: Name this error]
**Symptom:** `XYZ_TOTALLY_NEW_THING_TEST_MARKER: uses a completely fictitious pattern that has never been seen before`
**Cause:** [TODO: Add root cause]
**Fix instruction for AI retry:** "[TODO: Add specific fix steps]"

