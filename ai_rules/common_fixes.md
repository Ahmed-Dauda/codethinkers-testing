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
5. Every `{% url %}` tag MUST use namespace: `{% url 'app_name:name' %}`.
6. If 'list_select_related': Add `list_select_related = ('fk_field',)` to
   EVERY ModelAdmin.
7. If 'shows ForeignKey field(s)': Add the EXACT list_select_related tuple
   shown in the error message.
8. If 'references missing template': Ensure templates extend base.html and
   select a footer per your Footer Selection Rules.

Do NOT just change self_check to PASS — actually add the missing code.

9. If 'TemplateDoesNotExist: registration/login.html': You added LoginRequiredMixin or auth without the login template. Either:
   a) Add registration/login.html to the templates dict, OR
   b) Remove LoginRequiredMixin if the user didn't ask for authentication

9. If 'Model 'X' used but not imported': X is being referenced in
   views.py/urls.py/admin.py but was never defined as a class in
   models.py. Add the missing `class X(models.Model): ...` definition
   with real fields — do not just fix the import statement, the model
   itself is missing.   