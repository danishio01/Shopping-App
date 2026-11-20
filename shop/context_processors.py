
from .cart import get_cart


def cart_summary(request):

    items, total = get_cart(request)

    cart_count = sum(
        item["quantity"]
        for item in items
    )

    return {
        "cart_count": cart_count,
    }
