# UI Architecture

## General Rules
- Generate reusable templates using Django template inheritance.
- Avoid duplicating HTML across pages.
- Use Tailwind CSS for styling.
- Build responsive layouts.
- NEVER use placehold.co for images — use `https://picsum.photos/600/400?random={{ forloop.counter }}`.

## Base Template

⚠️ HARD REQUIREMENT: The `templates` dict in your JSON response MUST include
a `"base.html"` key. This is NOT optional — omitting it breaks every single
page in the app with TemplateDoesNotExist. Before finalizing your response,
check that `templates["base.html"]` exists.

`base.html` MUST contain:
- HTML structure with `<!DOCTYPE html>`
- Tailwind CSS CDN in `<head>`
- The navbar and footer selected per the UI Patterns Selection Table
  (see the UI Patterns rules) — this determines the actual HTML, not
  the description here
- Flash messages area
- `{% block content %}{% endblock %}` for page content
⚠️ CRITICAL: Every other template you generate MUST start with:

```html
{% extends "base.html" %}
{% block content %}
...page content...
{% endblock %}