from django.db import models

class Product(models.Model):
    name=models.CharField(max_length=50,null=False,blank=False,unique=True)
    slug=models.CharField(max_length=60,null=False,blank=True,unique=True)
    description=models.TextField(max_length=255,null=True,blank=True)
    details=models.TextField(max_length=255,null=True,blank=True)
    price=models.FloatField(null=False,blank=False)
    stock=models.IntegerField(default=1,null=True,blank=True)    
    active=models.BooleanField(default=True,null=False,blank=True)
    likes=models.IntegerField(default=0,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True,null=False,blank=True)

    class Meta:
        ordering=["-created_at","name"]
    
    def __str__(self):
        return f"{self.id}:{self.name}"
    
    
class Image(models.Model):
    name=models.CharField(max_length=255, null=False, blank=False)
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="images")
    file=models.ImageField(null=False, blank=True, upload_to="images/products")
    
    def __str__(self):
        return f"{self.product.name} - {self.name}"


