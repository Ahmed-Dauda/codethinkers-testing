# Code Generation Rules

## JSON Format
- Return ONLY valid JSON, no markdown, no explanation outside the JSON.
- All code content MUST use JSON-safe escaping:
  - Double quotes inside strings: `\"`
  - Backslashes: `\\`
  - Newlines: keep as real newlines in the JSON string
- Template HTML: Use single quotes for attributes where possible.
- NEVER use unescaped double quotes inside JSON string values.

## Python Code Style
- NEVER use trailing commas in import statements. Write `from django.urls import path` NOT `from django.urls import path,`
- Class-based views preferred (ListView, DetailView, CreateView, UpdateView, DeleteView).
- `.order_by('-id')` on ALL QuerySets.
- f-strings: use different quote types — `f"key: {dict['key']}"` NOT `f'key: {dict['key']}'`.
- `from django.db import models` when using Sum/Count/Avg.

## Template Naming Rules
- Template names MUST be model-specific: `post_list.html` NOT `list.html`. Always prefix with the lowercase model name.
- Template names MUST be bare filenames: `'post_list.html'` NOT `'app_name/post_list.html'`
- `home.html` is MANDATORY for every project.

## Response Format for Scaffold (new project)
```json
{
    "self_check": {
        "model_to_admin": "PASS - reason",
        "model_to_view": "PASS - reason",
        "view_to_url": "PASS - reason",
        "view_to_template": "PASS - reason",
        "url_template_links": "PASS - reason",
        "forms_present": "PASS - reason",
        "no_orphans": "PASS - reason"
    },
    "thinking": {
        "business_understanding": "...",
        "app_type": "CRUD Dashboard",
        "core_modules": ["..."],
        "database_design": "...",
        "admin_plan": "...",
        "page_plan": ["..."],
        "auth_plan": "...",
        "suggested_features": ["..."]
    },
    "app_name": "...",
    "models_py": "...",
    "views_py": "...",
    "admin_py": "...",
    "urls_py": "...",
    "tests_py": "...",
    "forms_py": "...",
    "templates": { "home.html": "...", "post_list.html": "...", ... }
}