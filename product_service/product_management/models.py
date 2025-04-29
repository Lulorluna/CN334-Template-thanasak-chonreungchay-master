from django.db import models


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50)
    players = models.CharField(max_length=20)
    age = models.PositiveIntegerField()
    play_time = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    production_date = models.DateField()
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
