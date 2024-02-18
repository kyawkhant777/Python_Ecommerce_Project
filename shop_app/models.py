
from django.db import models
from django.contrib.auth.models import User
import uuid


# Create your models here.
ORDER_CHOICES = [
    ('pending', 'Pending'),
    ('accepted', 'Accepted'),
    ('success', 'Success'),
    ('cancel', 'Cancel'),
]


class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=None)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(default=None)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField(default=None)
    qty = models.IntegerField(default=None)
    created_at = models.DateTimeField(default=None)
    
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField()
    user = models.ForeignKey(User,on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(default=None)

class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.IntegerField(default=None)
    total_qty = models.IntegerField(default=None)
    name = models.CharField(max_length=30, default=None)
    phone = models.IntegerField(default=None)
    address = models.TextField(default=None)
    status = models.CharField(max_length=20,choices=ORDER_CHOICES,default='pending')
    created_at = models.DateTimeField(default=None)
    
    def __str__(self):
        return str(self.name)
  


      
    