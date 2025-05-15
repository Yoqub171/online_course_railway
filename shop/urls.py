from django.urls import path
from .views import home, product_detail, order_detail, create_product, delete_product, edit_product, comment_create
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    path('category/<int:category_id>/', home, name='products_by_category'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('order/detail/<int:pk>/', order_detail, name='order_detail'),
    path('product/create/', create_product, name='create_product'),
    path('product/edit/<int:pk>/', edit_product, name='edit_product'),
    path('product/delete/<int:pk>/', delete_product, name='delete_product'),
    path('comment/create/<int:pk>', comment_create, name='comment_create')
]