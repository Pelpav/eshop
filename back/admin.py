from django.contrib import admin
from .models import Product, Image

# admin.site.register(Product)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'price', 'active']
    list_filter = ['active', ]
    search_fields = ['id', 'name']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'file', 'product']
    search_fields = ['id', 'name', 'product__name']