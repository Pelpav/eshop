from django.contrib import admin
from .models import Customer, MyUser

# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'avatar_tag', 'tel', 'address', 'city', 'zipcode', 'country']
    search_fields = ['user', 'tel', 'id']
    readonly_fields = ['avatar_tag', 'id', 'reviews_count', 'likes_count', 'orders_count']
    autocomplete_fields = ['user']
    list_display_links = ['id', 'user']
    fieldsets = (
        ("User information", {
            # "classes": ["collapse", "start-open"],
            "fields": ('id', 'user', 'avatar', 'avatar_tag')}
        ),
        ("Contacts", {
            # "classes": ["collapse", "start-open"],
            "fields": ('tel', 'address', 'city', 'zipcode', 'country')}
        ),
        ("Interactions", {
            "fields": ('reviews_count', 'likes_count', 'orders_count')}
        ),
    )


@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'avatar_tag']
    search_fields = ['user', 'id']
    fields = ['user', 'avatar', 'avatar_tag']
    readonly_fields = ['avatar_tag']
    list_display_links = ['id', 'user']
    autocomplete_fields = ['user']