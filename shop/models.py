from django.db import models
from decimal import Decimal


class Category(models.Model):
    title = models.CharField(max_length=100,unique=True)
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'categories'
        verbose_name = 'category'


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    image = models.ImageField(upload_to='products/')
    discount = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category,related_name='products',on_delete=models.SET_NULL,null=True,blank=True)
    
    def __str__(self):
        return self.name

    
    @property
    def discounted_price(self):
        if self.discount > 0:
            return self.price * Decimal(f'{1 - (self.discount / 100)}')
        return self.price
    
    @property
    def get_absolute_url(self):
        if self.image:
            return self.image.url
        return ''
    
    class Meta:
        verbose_name_plural = 'products'
        verbose_name = 'product'

