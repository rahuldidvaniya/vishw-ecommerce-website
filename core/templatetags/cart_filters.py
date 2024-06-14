from django import template

register = template.Library()

@register.filter
def cart_quantity(cart_data):
    # Return the sum of the quantities from the cart data dictionary
    return sum(item['qty'] for item in cart_data.values())
