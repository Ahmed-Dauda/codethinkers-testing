
from django import template

register = template.Library()

@register.filter
def endswith(value, suffix):
    """Returns True if value ends with the given suffix."""
    return str(value).lower().endswith(suffix)
