from django.contrib import admin
from .models import *

# admin.site.register(Product)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'price', 'active', 'category']
    list_filter = ['active', ]
    search_fields = ['id', 'name']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'file', 'product']
    search_fields = ['id', 'name', 'product__name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'active', 'image', 'parent']
    search_fields = ['id', 'name']
    list_filter = ['active']