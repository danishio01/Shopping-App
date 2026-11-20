
from django.urls import path
from . import views


app_name = "shop"


urlpatterns = [

    # Home page
    path(
        "",
        views.product_list,
        name="product_list"
    ),

    # Shopping cart page
    path(
        "cart/",
        views.cart_detail,
        name="cart_detail"
    ),

    # Add product
    path(
        "cart/add/<int:product_id>/",
        views.cart_add,
        name="cart_add"
    ),

    # Update quantity
    path(
        "cart/update/<int:product_id>/",
        views.cart_update,
        name="cart_update"
    ),

    # Remove product
    path(
        "cart/remove/<int:product_id>/",
        views.cart_remove,
        name="cart_remove"
    ),

]
