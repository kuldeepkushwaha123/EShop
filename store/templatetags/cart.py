from django import template

register = template.Library()


@register.filter(name='is_in_cart')
def is_in_cart(product,cart):
    keys = cart.keys()
    for id in keys:
        try:
            if int(id) == product.id:
                return True
        except:
            pass
    return False


@register.filter(name='cart_quantity')
def cart_quantity(product,cart):
    return cart[str(product.id)]


@register.filter(name='price_total')
def price_total(product,cart):
    return product.price * cart_quantity(product,cart)


@register.filter(name='total_cart_price')
def total_cart_price(products,cart):
    sum = 0
    for p in products:
        sum += price_total(p,cart)
    return sum





