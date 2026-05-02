"""
Data Population Script
Populates the database with 100,000 dummy transaction records from the last 6 months
"""
import os
import django
import random
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from api.models import Product, Transaction
from django.utils import timezone

def populate_data():
    """Populate database with products and transactions"""
    
    print("Starting data population...")
    
    # Create products if they don't exist
    products = []
    product_names = [
        'Laptop', 'Mouse', 'Keyboard', 'Monitor', 'USB Cable',
        'Headphones', 'Webcam', 'Microphone', 'SSD', 'RAM',
        'Graphics Card', 'Power Supply', 'Cooling Fan', 'Case', 'Motherboard'
    ]
    
    print("Creating products...")
    for name in product_names:
        product, created = Product.objects.get_or_create(
            name=name,
            defaults={
                'price': random.uniform(10, 2000),
                'stock': random.randint(100, 500)
            }
        )
        products.append(product)
        if created:
            print(f"  Created: {name}")
    
    # Create 100,000 transactions
    print("Creating 100,000 transactions...")
    
    transactions_list = []
    start_date = timezone.now() - timedelta(days=180)  # Last 6 months
    
    for i in range(100000):
        if i % 10000 == 0:
            print(f"  Progress: {i}/100000")
        
        random_date = start_date + timedelta(
            days=random.randint(0, 180),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59),
            seconds=random.randint(0, 59)
        )
        
        product = random.choice(products)
        quantity = random.randint(1, 10)
        
        transactions_list.append(
            Transaction(
                product=product,
                quantity=quantity,
                amount=product.price * quantity,
                timestamp=random_date,
                date=random_date.date()
            )
        )
    
    # Bulk create for performance
    Transaction.objects.bulk_create(transactions_list, batch_size=1000)
    
    print("✓ Data population completed!")
    print(f"  - Products created: {len(products)}")
    print(f"  - Transactions created: 100,000")


if __name__ == '__main__':
    populate_data()
