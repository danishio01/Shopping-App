
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST

from .models import Product
from .cart import get_cart, CART_SESSION_KEY


# 1. Display all available products
def product_list(request):
    products = Product.objects.filter(
        is_available=True,
        stock__gt=0
    )

    return render(
        request,
        "shop/product_list.html",
        {"products": products}
    )


# 2. Add a product to the cart
@require_POST
def cart_add(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    if not product.is_available or product.stock <= 0:
        messages.error(
            request,
            "This product is currently unavailable."
        )
        return redirect("shop:product_list")

    cart = request.session.get(CART_SESSION_KEY, {})

    key = str(product.id)

    current_quantity = int(cart.get(key, 0))

    if current_quantity >= product.stock:
        messages.warning(
            request,
            "You cannot add more than the available stock."
        )
        return redirect("shop:product_list")

    cart[key] = current_quantity + 1

    request.session[CART_SESSION_KEY] = cart

    messages.success(
        request,
        f"{product.name} added to cart!"
    )

    return redirect("shop:product_list")


# 3. Display cart items and subtotal
def cart_detail(request):

    items, total = get_cart(request)

    return render(
        request,
        "shop/cart_detail.html",
        {
            "items": items,
            "total": total,
        }
    )


# 4. Update the quantity of a product
@require_POST
def cart_update(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    cart = request.session.get(CART_SESSION_KEY, {})
    key = str(product.id)

    if key not in cart:
        messages.warning(
            request,
            "This product is not in your cart."
        )
        return redirect("shop:cart_detail")

    try:
        quantity = int(request.POST.get("quantity", 1))
    except (ValueError, TypeError):
        messages.error(
            request,
            "Please enter a valid quantity."
        )
        return redirect("shop:cart_detail")

    if quantity <= 0:
        cart.pop(key, None)

        messages.success(
            request,
            "Product removed from cart."
        )

    elif not product.is_available or product.stock <= 0:
        cart.pop(key, None)

        messages.warning(
            request,
            "This product is no longer available."
        )

    else:
        if quantity > product.stock:
            messages.warning(
                request,
                f"Only {product.stock} units are available."
            )

        cart[key] = min(quantity, product.stock)

        messages.success(
            request,
            "Cart quantity updated."
        )

    request.session[CART_SESSION_KEY] = cart

    return redirect("shop:cart_detail")


# 5. Remove a product from the cart
@require_POST
def cart_remove(request, product_id):

    cart = request.session.get(CART_SESSION_KEY, {})

    key = str(product_id)

    if key in cart:
        cart.pop(key)

        request.session[CART_SESSION_KEY] = cart

        messages.success(
            request,
            "Product removed successfully."
        )

    return redirect("shop:cart_detail")
