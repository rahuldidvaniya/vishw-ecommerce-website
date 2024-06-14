from django import template
import locale

register = template.Library()

@register.filter
def multiply(value, arg):
    try:
        value = locale.atof(value)
    except AttributeError:
        pass  # value is already a float, do nothing
    return value * arg

