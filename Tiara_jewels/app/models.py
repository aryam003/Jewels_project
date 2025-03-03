from django.db import models
from django.contrib.auth.models import User
from .constants import PaymentStatus
from django.db.models.fields import CharField
from django.utils.translation import gettext_lazy as _

# Create your models here.

class JewelryType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Abstract Jewelry class with a category
class Jewelry(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    material = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(JewelryType, on_delete=models.CASCADE)


    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)    
    product=models.ForeignKey(Jewelry,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # Add this field

    def __str__(self):
        return self.name
    

    def __str__(self):
        return self.name  
    
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    size = models.IntegerField(default=10)


class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    price=models.IntegerField()
    status=CharField(
        _("Payment Status"),
        default=PaymentStatus.PENDING,
        max_length=254,
        blank=False,
        null=False
    )
    provider_order_id = models.CharField(
        _("Order ID"), max_length=40, null=False,blank=False
    )
    payment_id = models.CharField(
        _("Payment ID"),max_length=36, null=False, blank=False
    )
    signature_id = models.CharField(
        _("Signature ID"), max_length=128, null=False, blank=False
    )

class Buy(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Jewelry,on_delete=models.CASCADE)
    price=models.IntegerField()
    date=models.DateField(auto_now_add=True)   
    quantity = models.PositiveIntegerField(default=1) 
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True)  # Make it nullable
    # address = models.ForeignKey(Address, on_delete=models.CASCADE)
    is_confirmed = models.BooleanField(default=False)
    order=models.ForeignKey(Order,on_delete=models.CASCADE,null=True)    