from django.contrib import admin
from .models import Product, Category, Comment
from django.contrib.auth.models import User,Group


admin.site.register(Category)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'discount', 'category']
    search_fields = ['name']
    list_filter = ['price']

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'content', 'rating', 'created_at')
    search_fields = ('user__username', 'text') 

admin.site.register(Comment, CommentAdmin)
