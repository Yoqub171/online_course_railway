from django import forms
from .models import Order, Product, Comment

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'phone', 'address', 'quantity']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'discount', 'category', 'quantity']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('created_at', 'updated_at', 'product')