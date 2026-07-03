from django.db import models

SIZE_CHOICES = [
    ('1L', '1 Litre'),
    ('5L', '5 Litres'),
    ('10L', '10 Litres'),
    ('20L', '20 Litres'),
]

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    location = models.CharField(max_length=255)
    is_credit_customer = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)
    size = models.CharField(max_length=3, choices=SIZE_CHOICES)
   
    def __str__(self):
        return f"{self.size} - KES {self.price}"
