from django import template

register = template.Library()

@register.filter
def has_ext(filename, ext):
    return filename.lower().endswith(f".{ext.lower()}")


