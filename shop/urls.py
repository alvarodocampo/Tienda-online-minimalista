from django.urls import path
from .views import (
    product_list,
    product_detail,
    add_to_cart,
    cart_detail,
    create_order,
    payment_page,
    payment_success,
    remove_from_cart,
    )

urlpatterns = [
    path('', product_list, name='product_list'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_detail, name='cart_detail'),
    path('order/create/', create_order, name='create_order'),
    path('payment/<int:order_id>/', payment_page, name='payment_page'),
    path('payment/<int:order_id>/success/', payment_success, name='payment_success'),
    path('cart/remove/<int:product_id>/',remove_from_cart,name='remove_from_cart'),
]