# Understanding Existing Projects

When modifying an existing project (incremental changes):

1. **Review ALL existing models, views, URLs, templates** — understand what's already there.
2. **Follow existing naming conventions and patterns** — match the code style.
3. **Preserve ALL existing code** — only add/modify what's needed. Never drop existing functionality.
4. **If adding to existing files, provide COMPLETE file content** (not diffs, not partial).
5. **Maintain consistent URL namespacing** — use the same `app_name` prefix.
6. **Match existing template structure** — same navbar, footer, Tailwind classes, block names.
7. **Every template MUST extend the same base template** used elsewhere in the project with the same block names.
8. **For every model added or touched**, verify: admin registration, URL patterns, views, and templates all exist.
9. **Every `{% url 'name' %}` tag** must match a `name=` you actually defined. Cross-check every one.
10. **Every view referenced in urls.py** must exist in views.py content.