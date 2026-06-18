from django.shortcuts import render, get_object_or_404
from .models import Product,Order,OrderItem
from django.shortcuts import redirect


def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {
        'products': products
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    return render(request, 'shop/product_detail.html', {
        'product': product
    })

def add_to_cart(request, product_id):
    cart = request.session.get('cart', [])

    cart.append(product_id)

    request.session['cart'] = cart

    return redirect('product_list')

def cart_detail(request):
    cart = request.session.get('cart', [])

    cart_items = []
    total = 0

    for product_id in cart:
        product = Product.objects.get(id=product_id)

        encontrado = False

        for item in cart_items:
            if item['product'].id == product.id:
                item['quantity'] += 1
                item['subtotal'] = item['quantity'] * item['product'].price
                encontrado = True

        if not encontrado:
            cart_items.append({
                'product': product,
                'quantity': 1,
                'subtotal': product.price
            })

    for item in cart_items:
        total += item['subtotal']

    return render(request, 'shop/cart_detail.html', {
        'cart_items': cart_items,
        'total': total
    })

def create_order(request):
    cart = request.session.get('cart', [])

    if not cart:
        return redirect('cart_detail')

    order = Order.objects.create(user=request.user)

    for product_id in cart:
        product = Product.objects.get(id=product_id)

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=1,
            price=product.price
        )

    request.session['cart'] = []

    return redirect('payment_page', order_id=order.id)

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', [])

    if product_id in cart:
        cart.remove(product_id)

    request.session['cart'] = cart

    return redirect('cart_detail')

def payment_page(request, order_id):
    order = Order.objects.get(id=order_id)

    return render(request, 'shop/payment_page.html', {
        'order': order
    })

def payment_success(request, order_id):
    order = Order.objects.get(id=order_id)

    order.paid = True
    order.status = 'paid'
    order.save()

    return render(request, 'shop/payment_success.html', {
        'order': order
    })