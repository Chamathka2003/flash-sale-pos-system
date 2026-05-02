from django.contrib import admin
from .models import Product, Transaction, Order, OrderItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'amount', 'timestamp']
    list_filter = ['date']
    search_fields = ['product__name']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['order_number']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'subtotal']
    list_filter = ['created_at']
    search_fields = ['order__order_number', 'product__name']
