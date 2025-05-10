from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from decimal import Decimal, InvalidOperation
from .models import Product, Order, Category
from .forms import OrderForm


def home(request, category_id=None):
    search_query = request.GET.get('q', '')
    categories = Category.objects.all()

    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()

    if search_query:
        products = products.filter(name__icontains=search_query)

    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'shop/home.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.product = product

            if product.discount > 0:
                total_price = product.discounted_price * order.quantity
            else:
                total_price = product.price * order.quantity

            order.total_price = total_price
            order.save()

            return redirect('order_success', order_id=order.id)
    else:
        form = OrderForm()

    context = {
        'product': product,
        'form': form
    }
    return render(request, 'shop/detail.html', context)


def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    try:
        total_price = Decimal(order.total_price)
    except (InvalidOperation, ValueError, TypeError):
        total_price = Decimal('0.00')

    return HttpResponse(
        f"Thank you for your order! Your order ID is {order.id} and total price is ${total_price:.2f}."
    )
