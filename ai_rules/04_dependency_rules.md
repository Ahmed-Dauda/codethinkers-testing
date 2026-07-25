# Dependency Rules — Everything Must Connect

## Required Connections
1. **MODEL → ADMIN**: Every model has `@admin.register()` with full config including list_select_related for FK fields.
2. **MODEL → VIEW**: Every model has the views specified by the user's requirements. Public apps may need ListView + DetailView. Private apps may only need admin. Generate ONLY what the user asked for — do not auto-add CRUD.
3. **VIEW → URL**: Every view has a `path()` with correct `name=` pattern.
4. **VIEW → TEMPLATE**: Every `template_name` references an existing template file.
5. **URL → TEMPLATE**: Every `{% url %}` tag matches a defined `name=` value using namespace.
6. **MODEL → FORM**: Every model has a ModelForm if CreateView/UpdateView exist.
7. **APP → ROOT URLS**: Every app's urls.py is wired into the root urls.py via `include()`.
8. **APP → INSTALLED_APPS**: Every app is registered in settings.py INSTALLED_APPS.
9. **VIEWS → IMPORTS**: `views.py` MUST import all class-based view parents (ListView, DetailView, CreateView, UpdateView, DeleteView). `urls.py` MUST have `from . import views`. `admin.py` MUST have `from .models import ModelName` for every registered model. `forms.py` MUST import every model it creates a form for.
10. **HOME PAGE**: Every project MUST have a home page at the root URL (`name='home'`) with a `home.html` template. The home view MUST query real data (not a static page).

- When using `redirect('view_name', pk=...)` or `reverse('view_name', kwargs={'pk': ...})`, always use `pk` as the parameter name. URL patterns use `<int:pk>` by convention. Never use `quiz_id`, `post_id`, etc. — always `pk`.

## Completeness Verification (HARD REQUIREMENT)
Before returning JSON, mentally trace:
- Every URL name → matching `path()` in urls.py
- Every view class → actually exists in views.py
- Every template reference → actual file in templates dict
- Every `{% url %}` tag → uses correct namespace prefix
- `from . import views` exists in every app's urls.py
- `home.html` exists in templates dict with a HomeView wired to `name='home'`
- A model with no admin, a URL with no view, or a template with broken links = INCOMPLETE. Fix before returning.