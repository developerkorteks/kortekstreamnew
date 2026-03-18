import json
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='replace')
def replace(value, arg):
    """
    Usage: {{ value|replace:"old,new" }}
    """
    if not isinstance(value, str):
        return value
        
    parts = arg.split(',')
    if len(parts) != 2:
        return value
    
    old, new = parts[0], parts[1]
    return value.replace(old, new)

@register.filter(name='to_json')
def to_json(value):
    """
    Safe JSON dumping for template variables.
    """
    try:
        return mark_safe(json.dumps(value))
    except (TypeError, ValueError):
        return "{}"
