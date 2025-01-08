from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe
from .models import *

class AdminImageWidget(AdminFileWidget):
    def render(self, name, value, attrs=None, renderer=None):
        output = []
        if value and getattr(value, "url", None):
            image_url = value.url
            output.append(
                f'<a href="{image_url}" target="_blank">'
                f'<img src="{image_url}" width="50" height="50" '
                f'style="object-fit: cover;"/> </a>')
        output.append(super(AdminFileWidget, self).render(name, value, attrs, renderer))
        return mark_safe(u''.join(output))


class ImageInline(admin.TabularInline):
    model = Image
    # fields = ['name']
    formfield_overrides = {
        models.ImageField: {'widget': AdminImageWidget}
    }
    extra = 0

# admin.site.register(Product)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'price', 'active', 'category']
    list_filter = ['active', ]
    search_fields = ['id', 'name']
    inlines = [ImageInline]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'img_display', 'product']
    search_fields = ['id', 'name', 'product__name']
    read_only_fields = ['img_display']
    


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'active', 'image', 'parent']
    search_fields = ['id', 'name']
    list_filter = ['active']