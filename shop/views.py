from django.shortcuts import render, get_object_or_404
from .models import Product
from django.http.response import HttpResponse


def home(request):
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'shop/home.html',context)


def product_detail(request, product_id): 
    try:
        product = Product.objects.get(id=product_id)
        context = {'product': product}
        return render(request, 'shop/detail.html', context)
    except Product.DoesNotExist:
        return HttpResponse('Product Not Found')

    