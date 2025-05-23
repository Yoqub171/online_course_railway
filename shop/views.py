from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import Product, Category
from .forms import OrderForm, ProductForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.db.models.functions import Round
from .utils import product_rating_filter



def home(request, category_id=None):
    search_query = request.GET.get('q', '')
    filter_type = request.GET.get('filter','')
    categories = Category.objects.all()

    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()

    if search_query:
        products = products.filter(name__icontains=search_query)

    products = products.annotate(average_rating = Round(Avg('comments__rating'), precision = 2))

    products = product_rating_filter(filter_type, products)

    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'shop/home.html', context)


def product_detail(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        related_products = Product.objects.filter(category = product.category).exclude(id = product.id)
        form = OrderForm()

        context = {
            'product': product,
            'form': form,
            'related_products': related_products
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

                return redirect('shop:product_detail', pk=product.pk)

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
            return redirect('shop:home')

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
            return redirect('shop:product_detail', product_id=product.pk)


    context = {
        'form': form,
        'product': product
    }

    return render(request, 'shop/product/edit.html', {'form': form})

    


@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('shop:home') 
    return render(request, 'shop/product/delete.html', {'product': product})

def comment_create(request, pk):
    product = get_object_or_404(Product, id=pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.user = request.user
            comment.save()
            return redirect('shop:product_detail', product_id=product.id)
        else:
            print(form.errors) 
    else:
        form = CommentForm()
    
    return render(request, 'shop/detail.html', {'form': form})  

