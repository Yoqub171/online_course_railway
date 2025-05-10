from django.urls import path
from .views import home, product_detail, order_success
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    path('category/<int:category_id>/', home, name='products_by_category'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('order/success/<int:order_id>/', order_success, name='order_success'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
