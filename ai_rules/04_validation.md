# Self-Check Before Responding

Verify EVERY item below. If any fails, FIX THE CODE, not the self-check report. Never report PASS unless it is genuinely true.

1. **model_to_admin**: Every model has `@admin.register()` with list_display (3-5 fields), list_filter, search_fields, list_select_related for all FK fields shown.
2. **model_to_view**: Every model has the views specified by the user's requirements. Public apps may need ListView + DetailView. Private apps may only need admin. Generate ONLY what the user asked for — do not auto-add CRUD.
3. **view_to_url**: Every view has a `path()` with correct name= pattern ({model}_list, {model}_detail, etc.).
4. **view_to_template**: Every `template_name` references an existing template key — same spelling, same case, bare filename only.
5. **url_template_links**: Every `{% url 'name' %}` tag matches a defined name= using app_name namespace.
6. **forms_present**: Every CreateView/UpdateView has a corresponding ModelForm.
7. **no_orphans**: Every template is referenced by at least one view.
8. **auth_complete**: If LoginRequiredMixin is used, templates includes `registration/login.html` and navbar has login/logout links. If no auth, this is N/A - PASS.

## Performance Checks
- **N+1 queries**: select_related/prefetch_related in get_queryset() for all FK/M2M fields shown in templates
- **Pagination**: paginate_by=25 on every ListView
- **Indexed filters**: db_index=True on filtered/ordered fields
- **No queries in template loops**: annotate counts instead of calling .count() in `{% for %}`
- **list_select_related**: on all admin FK fields in list_display/list_filter
- **Static weight**: Tailwind CDN loaded once, no duplicate scripts

## Auth Requirements
- If LoginRequiredMixin/@login_required/request.user filtering is used ANYWHERE:
  1. Root urls.py must include `path('accounts/', include('django.contrib.auth.urls'))`
  2. Templates must include `registration/login.html` (bare key, not app-prefixed)
  3. Navbar must have `{% url 'login' %}` / `{% url 'logout' %}` links
  4. LOGIN_REDIRECT_URL set in settings.py
  5. If user-owned content, also add signup view + `registration/signup.html`
- If NO view uses request.user: skip all auth scaffolding. Do not add it.