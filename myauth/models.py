from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

# Create your models here.
class MyUser(models.Model):
    user = models.OneToOneField(User, null=False, blank=False, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='images/users/', null=True, blank=True)
    
    def avatar_tag(self):
        if not self.avatar:
            return ''
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
                url = self.avatar.name.url,
                width=50,
                height=50,
            )
        ) 
    
    def __str__(self):
        return f"{self.user.username}"


class Customer(models.Model):
    user = models.OneToOneField(User, null=False, blank=False, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='images/customers/', null=True, blank=True)
    address = models.CharField(max_length=30, null=True, blank=True)
    zipcode = models.CharField(max_length=6, null=True, blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)
    country = models.CharField(max_length=20, null=True, blank=True)
    tel = models.CharField(max_length=20, null=True, blank=True)

    def avatar_tag(self):
        if not self.avatar:
            return '-'
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
                url = self.avatar.name.url,
                width=50,
                height=50,
            )
        )
    
    @property
    def reviews_count(self):
        from back.models import Review
        return Review.objects.filter(email=self.user.email).count()

    @property
    def likes_count(self):
        from back.models import Like
        return Like.objects.filter(liked=True, email=self.user.email).count()
    
    @property
    def orders_count(self):
        from back.models import Order
        return f"{Order.objects.filter(customer=self, completed=True).count()} / {Order.objects.filter(customer=self).count()}"
    
    def __str__(self):
        return f"{self.user.username}"
