from django.contrib import admin
from .models import Product, Category
from django.contrib.auth.models import User,Group



admin.site.register(Category)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'discount', 'category']
    search_fields = ['name']
    list_filter = ['price']
