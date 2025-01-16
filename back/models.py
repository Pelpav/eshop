from django.db import models
from django.utils.safestring import mark_safe
from django_countries.fields import CountryField
from django.utils.timezone import now
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, unique=True)
    slug = models.CharField(max_length=60, null=False, blank=True, unique=True)
    description = models.TextField(max_length=255, null=True, blank=True)
    details = models.TextField(max_length=255, null=True, blank=True)
    price = models.FloatField(null=False, blank=False)
    stock = models.IntegerField(default=1, null=True, blank=True)
    active = models.BooleanField(default=True, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=True)
    category = models.ForeignKey('Category', null=True, blank=False,
                                 on_delete=models.SET_NULL, related_name='products')
    
    class Meta:
        ordering = ["-created_at", "name"]
    
    def __str__(self):
        return f"{self.id} : {self.name}"

    @property
    def promo_price(self):
        return self.price + self.price * 0.09

    @property
    def first_image(self):
        if self.images.all():
            return self.images.all()[0].file.url
        else:
            return ''
    
    @property
    def reviews_rate(self):
        if not self.reviews.all():
            return 0
        from django.db.models import Avg
        return self.reviews.all().aggregate(mean=Avg('rate'))['mean']
    
    @property
    def reviews_count(self):
        return self.reviews.count()

    @property
    def likes_total(self):
        return self.likes.filter(liked=True).count()
    
    @property
    def orders_count(self):
        return f"{self.orders.filter(completed=True).count()} / {self.orders.count()}"
    
    @property
    def solde_amount(self):
        solde = 0
        for order in self.orders.filter(completed=True):
            solde += sum([item.quantity * item.price for item in OrderDetails.objects.filter(order=order)])
        return solde

    

class Image(models.Model):
    name = models.CharField(max_length=30, null=False, blank=False)
    file = models.ImageField(null=False, blank=True, upload_to="images/products/")
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="images")
    
    def __str__(self):
        return f"{self.name} de {self.product.name}"

    @property
    def img_display(self):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
                url = self.file.url,
                width=50,
                height=50,
            )
        ) 
    

class Category(models.Model):
    name = models.CharField(max_length=45, null=False, blank=False, unique=True)
    slug = models.CharField(max_length=50, null=False, blank=False, unique=True)
    active = models.BooleanField(default=True, null=False, blank=False)
    created_at = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    image = models.ImageField(null=True, blank=True, upload_to='images/categories/')
    parent = models.ForeignKey('Category', null=True, blank=True, 
                               related_name='subcategories', on_delete=models.SET_NULL)
    
    class Meta:
        verbose_name_plural = "categories"
        ordering = ["-created_at", "name"]
    
    def __str__(self):
        return f"{self.name}"
    

class Order(models.Model):
    reference = models.CharField(max_length=30, null=False, blank=False, unique=True)
    coupon = models.ForeignKey('Coupon', null=True, blank=True, on_delete=models.SET_NULL, 
        related_name='orders')
    customer = models.ForeignKey('myauth.Customer', null=True, blank=False, 
        on_delete=models.SET_NULL, related_name='orders')
    created_at = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    products = models.ManyToManyField('Product', through='OrderDetails', related_name='orders')
    completed = models.BooleanField(default=False, null=True, blank=False)

    class Meta:
        ordering = ["-created_at", "reference"]
    
    @property
    def total(self):
        return self.subtotal + self.shipping - self.reduction
    
    @property
    def shipping(self):
        # from django.db.models import Sum
        # if self.deliveries.all():
        #     return self.deliveries.all().aggregate(sum=Sum('price'))['sum']
        return 10
    
    @property
    def subtotal(self):
        items = OrderDetails.objects.filter(order=self)
        return sum([item.price * item.quantity for item in items])
    
    @property
    def reduction(self):
        if self.coupon:
            if self.coupon.coupon_type.id == 1:
                return self.subtotal * self.coupon.discount / 100
            else:
                return self.coupon.discount
        return 0
        
    @property
    def orderDetails(self):
       if self.OrderDetails.all():
           return self.OrderDetails.all()

    def __str__(self):
        return f"{self.reference}"
    
    @property
    def products_count(self):
        return self.products.count()


class OrderDetails(models.Model):
    order = models.ForeignKey('Order', null=True, blank=False, on_delete=models.SET_NULL)
    product = models.ForeignKey('Product', null=True, blank=False, on_delete=models.SET_NULL)
    quantity = models.SmallIntegerField(default=1, null=True, blank=False)
    price = models.SmallIntegerField(default=1, null=True, blank=False)
    
    class Meta:
        verbose_name = "Order details"
        verbose_name_plural = "Orders details"

    def __str__(self):
        return f"{self.order.reference} : {self.product.name} x {self.quantity}"
    
    @property
    def total(self):
        return self.quantity * self.price
    

class Arrival(models.Model):
    created_at = models.DateTimeField(null=False, blank=False, auto_now=True)
    closed_at = models.DateTimeField(null=False, blank=False, auto_now=True)
    is_closed = models.BooleanField(default=False, null=True, blank=False)
    products = models.ManyToManyField("Product", related_name="arrivals", 
                                      through='ArrivalDetails')

    class Meta:
        ordering = ["-created_at", ]

    def __str__(self):
        return f"{self.id}"

    @property
    def products_count(self):
        return self.products.count()


class ArrivalDetails(models.Model):
    arrival = models.ForeignKey("Arrival", null=True, blank=False, on_delete=models.SET_NULL)
    product = models.ForeignKey("Product", null=True, blank=False, on_delete=models.SET_NULL)
    quantity = models.SmallIntegerField(default=1, null=False, blank=False)

    class Meta:
        verbose_name = "Arrival details"
        verbose_name_plural = "Arrivals details"

    def __str__(self):
        return f"{self.arrival.id} : {self.product.name} x {self.quantity}"
    

class Payment(models.Model):
    reference = models.CharField(max_length=64, null=False, blank=False, unique=True)
    order = models.OneToOneField('Order', on_delete=models.PROTECT, related_name='payment')
    payed_at = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    mode = models.CharField(max_length=30, default='Cash', null=False, blank=False)
    details = models.TextField(max_length=255, null=True, blank=True)
    class Meta:
        ordering = ["-payed_at", "reference"]

    def __str__(self):
        return f"Payment of {self.order} at {self.payed_at.strftime('%Y-%m-%d')}"
    

class Delivery(models.Model):
    address = models.CharField(max_length=30, null=False, blank=False)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    country = CountryField(multiple=False, blank=True, null=True)
    zipcode = models.CharField(max_length=30, null=False, blank=False)
    city = models.CharField(max_length=30, null=False, blank=False)
    price = models.FloatField(default=0, null=False, blank=False)
    state = models.CharField(max_length=30, null=True, blank=True)
    order = models.ForeignKey('Order', null=False, blank=False, on_delete=models.PROTECT, 
        related_name='deliveries')
    delivered_by = models.ForeignKey('myauth.MyUser', null=True, blank=True, on_delete=models.SET_NULL, 
        related_name='+')
    delivered_at = models.DateTimeField(null=True, blank=True, default=now)
    
    class Meta:
        ordering = ["-delivered_at", "-state"]
        verbose_name_plural = "deliveries"
    
    def __str__(self):
        return f"Delivery of {self.order.reference} : {self.state}"
    

class Coupon_type(models.Model):
    name = models.CharField(max_length=30, null=False, blank=False, unique=True)

    class Meta:
        verbose_name_plural = "coupons types"

    def __str__(self):
        return f"{self.name}"


class Coupon(models.Model):
    code = models.CharField(max_length=30, null=False, blank=False, unique=True)
    description = models.TextField(null=True, blank=True)
    coupon_type = models.ForeignKey('Coupon_type', null=True, blank=True, on_delete=models.SET_NULL)
    discount = models.SmallIntegerField(default=1, null=True, blank=False)
    max_usage = models.SmallIntegerField(default=1, null=True, blank=False)
    validity = models.DateTimeField(null=False, blank=False)
    is_valid = models.BooleanField(default=True, null=False, blank=False)
    created_at = models.DateTimeField(null=False, blank=False, auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.code}"
    

class Review(models.Model):
    rate = models.FloatField(null=False, blank=False, default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    comment = models.TextField(null=True, blank=True)
    name = models.CharField(max_length=30, null=False, blank=False)
    email = models.CharField(max_length=30, null=False, blank=False)
    product = models.ForeignKey('Product', null=False, blank=False, 
        on_delete=models.CASCADE, related_name='reviews')
    created_at = models.DateTimeField(null=False, blank=False, auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-rate"]

    def __str__(self):
        return f"{self.product.name} rated {self.rate} at {self.created_at.strftime('%Y-%m-%d, %H:%M:%S')}"


    @property
    def user_photo(self):
        from myauth.models import Customer
        customer = Customer.objects.get(user__email=self.email)
        if customer and customer.avatar:
            return customer.avatar.url
        return ''


class Like(models.Model):
    email = models.CharField(max_length=30, null=False, blank=False)
    liked = models.BooleanField(default=True, null=False, blank=False)
    product = models.ForeignKey('Product', null=False, blank=False, 
        on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(null=False, blank=False, auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-liked"]

    def __str__(self):
        return f"{self.product.name}" + ("liked" if self.liked else "unliked") + f" at {self.created_at.strftime('%Y-%m-%d, %H:%M:%S')}"


class Alerts(models.Model):
    status = models.CharField(max_length=30, null=False, blank=False)
    type = models.CharField(max_length=30, null=False, blank=False)
    details = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    traited_at = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.PROTECT, 
        related_name='+')
    
    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = 'alerts'

    def __str__(self):
        return f"{self.id} at {self.created_at.strftime('%Y-%m-%d, %H:%M:%S')} : {self.status}"


class Faqs(models.Model):
    type = models.CharField(max_length=30, null=False, blank=False)
    question = models.TextField(null=True, blank=True)
    answer = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(null=False, blank=False, auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Faqs'

    def __str__(self):
        return f"{self.question}"
    

class Filter_Price(models.Model):
    min = models.FloatField(null=True, blank=False)
    max = models.FloatField(null=True, blank=False)

    class Meta:
        verbose_name = 'Price bracket'
        verbose_name_plural = 'Prices brackets'
        ordering = ['min', 'max']

    def __str__(self):
        return f"{self.min} - {self.max}"
    
    @property
    def products_count(self):
        return Product.objects.filter(active=True, price__gte=self.min, price__lte=self.max).count()