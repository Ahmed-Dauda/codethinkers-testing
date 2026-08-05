# UI Architecture

## General Rules
- Generate reusable templates using Django template inheritance.
- Avoid duplicating HTML across pages.
- Use Tailwind CSS for styling.
- Build responsive layouts.
- NEVER use placehold.co for images — use `https://picsum.photos/600/400?random={{ forloop.counter }}`.

## Base Template

base.html is provided automatically by the platform - you do NOT need to
generate it, and you should NOT include a base.html key in the templates
dict. It already contains: full HTML structure, Tailwind CSS CDN, Alpine.js
CDN, a properly working mobile hamburger nav, the correct navbar and footer
selected automatically per app type, and a flash messages area.

CRITICAL: Every template you DO generate MUST start with:

```html
{% extends "base.html" %}
{% block content %}
...page content...
{% endblock %}
```

Never redefine the navbar, footer, or html/head/body structure in any page
template - base.html already owns all of that.

- For interactive components (dropdowns, modals, tabs, accordions, toasts), see `12_interactive_components.md` for pre-built accessible Alpine.js patterns. Use those patterns as-is instead of inventing new JS.

