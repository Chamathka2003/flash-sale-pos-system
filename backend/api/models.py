from django.db import models
from django.utils import timezone

class Product(models.Model):
    """Product model for inventory management"""
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'products'


class Transaction(models.Model):
    """Transaction model for tracking all purchases"""
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} units on {self.timestamp}"

    class Meta:
        db_table = 'transactions'
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['product', 'date']),
        ]


class Order(models.Model):
    """Order model for POS checkout"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    order_number = models.CharField(max_length=50, unique=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.order_number}"

    class Meta:
        db_table = 'orders'


class OrderItem(models.Model):
    """OrderItem model for items in each order"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    class Meta:
        db_table = 'order_items'
