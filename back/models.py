from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, unique=True)
    slug = models.CharField(max_length=60, null=False, blank=True, unique=True)
    description = models.TextField(max_length=255, null=True, blank=True)
    details = models.TextField(max_length=255, null=True, blank=True)
    price = models.FloatField(null=False, blank=False)
    stock = models.IntegerField(default=1, null=True, blank=True)
    active = models.BooleanField(default=True, null=False, blank=True)
    likes = models.IntegerField(default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=True)
    category = models.ForeignKey('Category', null=True, blank=False,
                                 on_delete=models.SET_NULL, related_name='products')
    
    class Meta:
        ordering = ["-created_at", "name"]
    
    def __str__(self):
        return f"{self.id} : {self.name}"
    

class Image(models.Model):
    name = models.CharField(max_length=30, null=False, blank=False)
    file = models.ImageField(null=False, blank=True, upload_to="images/products/")
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="images")
    
    def __str__(self):
        return f"{self.name} de {self.product.name}"
    

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
    created_at = models.DateTimeField(null=False, blank=False, auto_now=True)
    completed = models.BooleanField(default=False, null=True, blank=False)
    products = models.ManyToManyField("Product", related_name="orders", through='OrderDetails')

    class Meta:
        ordering = ["-created_at", "reference"]

    def __str__(self):
        return f"{self.reference}"
    

class OrderDetails(models.Model):
    order = models.ForeignKey("Order", null=True, blank=False, on_delete=models.SET_NULL)
    product = models.ForeignKey("Product", null=True, blank=False, on_delete=models.SET_NULL)
    quantity = models.SmallIntegerField(default=1, null=False, blank=False)
    price = models.FloatField(null=False, blank=False)

    class Meta:
        verbose_name = "Order details"
        verbose_name_plural = "Orders details"

    def __str__(self):
        return f"{self.order.reference} : {self.product.name} x {self.quantity}"
    

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
    
