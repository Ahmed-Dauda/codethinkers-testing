from django.utils.safestring import mark_safe

def generate_rendered_html(project):
    html_code = project.html_code.strip().lower()
    is_full_html = html_code.startswith("<!doctype") or "<html" in html_code

    if is_full_html:
        return mark_safe(project.html_code)

    external_css = f'<link rel="stylesheet" href="{project.external_css_url}">' if getattr(project, 'external_css_url', '') else ''
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  {external_css}
  <style>{project.css_code}</style>
</head>
<body>
  {project.html_code}
  <script>{project.js_code}</script>
</body>
</html>"""

    return mark_safe(full_html)
