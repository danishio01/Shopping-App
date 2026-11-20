
from decimal import Decimal
from .models import Product


CART_SESSION_KEY = "shopping_cart"


def get_cart(request):
    cart_data = request.session.get(CART_SESSION_KEY, {})

    products = Product.objects.filter(
        id__in=cart_data.keys(),
        is_available=True,
        stock__gt=0,
    )

    items = []
    total = Decimal("0.00")

    for product in products:
        key = str(product.id)

        try:
            quantity = int(cart_data.get(key, 0))
        except (ValueError, TypeError):
            quantity = 0

        quantity = min(max(quantity, 0), product.stock)

        if quantity == 0:
            continue

        line_total = product.price * quantity

        items.append({
            "product": product,
            "quantity": quantity,
            "line_total": line_total,
        })

        total += line_total

    return items, total
