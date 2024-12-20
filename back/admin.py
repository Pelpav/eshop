from django.contrib import admin
from .models import Product

# admin.site.register(Product)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=["id","slug","name","price","stock","active"]
    list_filter=["active"]
    search_fields=["id","name"]
    list_per_page=10
    list_display_links=["name"]
    list_max_show_all=100