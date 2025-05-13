from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import Product, Order, Category
from .forms import OrderForm, ProductForm
from django.contrib.auth.decorators import login_required

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
    try:
        product = Product.objects.get(id=product_id)
        form = OrderForm()
        context = {
            'product': product,
            'form': form
        }
        return render(request, 'shop/detail.html', context)
    except Product.DoesNotExist:
        return HttpResponse('Product Not Found')


def order_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = OrderForm()

    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            order.product = product

            if product.quantity < order.quantity or order.quantity == 0:
                messages.add_message(
                    request,
                    messages.ERROR,
                    'Dont have enough product quantity'
                )
            else:
                product.quantity -= order.quantity
                product.save()

                order.save()

                messages.add_message(
                    request,
                    messages.SUCCESS,
                    'Item successfully ordered'
                )

                return redirect('product_detail', pk=product.pk)

    context = {
        'form': form,
        'product': product
    }

    return render(request, 'shop/detail.html', context)



@login_required
def create_product(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Mahsulot muvaffaqiyatli qo\'shildi!')
            return redirect('home')

    context = {
        'form': form
    }

    return render(request, 'shop/product/create.html', context)


@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(instance=product)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                'Product updated successfully'
            )
            return redirect('product_detail', pk=product.pk)

    context = {
        'form': form,
        'product': product
    }

    return render(request, 'shop/product/edit.html', context)


@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('home') 
    return render(request, 'shop/product/delete.html', {'product': product})
