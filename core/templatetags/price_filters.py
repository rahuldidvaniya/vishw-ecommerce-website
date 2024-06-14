from django import template

register = template.Library()

@register.filter
def convert_price(price):
    return float(price.replace(',', ''))
