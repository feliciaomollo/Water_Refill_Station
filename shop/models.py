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
    
class Sale(models.Model): #The ORM automatically handles the plural (sales) for database table naming and admin display.
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    is_cancelled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.customer} - {self.product} on {self.date}"
    
class TankLevel(models.Model):
    SOURCE_CHOICES = [
        ('manual', 'Manual Entry'),
        ('api', 'API/Sensor'),
    ]

    level_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    recorded_at = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=10, choices=SOURCE_CHOICES, default='manual')

    def __str__(self):
        return f"{self.level_percentage}% at {self.recorded_at}"
