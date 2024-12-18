from django.db import models
from django.contrib.auth.models import User

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

    def __str__(self):
        return self.name
    
class Buy(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Jewelry,on_delete=models.CASCADE)
    price=models.IntegerField()
    date=models.DateField(auto_now_add=True)   

    def __str__(self):
        return self.name  