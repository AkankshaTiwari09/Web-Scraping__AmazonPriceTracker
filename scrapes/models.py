from django.db import models

# Create your models here.

class Product(models.Model):
    name=models.TextField(max_length=100)
    old_price=models.CharField(max_length=100)
    new_price=models.CharField(max_length=100)
    discount=models.CharField(max_length=100)
    url=models.CharField(max_length=1000,default='https://www.amazon.in')
