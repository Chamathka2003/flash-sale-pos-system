import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from api.models import Product

# Create sample products
products_data = [
    {'name': 'Laptop', 'price': 999.99, 'stock': 50},
    {'name': 'Phone', 'price': 699.99, 'stock': 100},
    {'name': 'Tablet', 'price': 399.99, 'stock': 75},
    {'name': 'Monitor', 'price': 299.99, 'stock': 60},
    {'name': 'Keyboard', 'price': 99.99, 'stock': 150},
]

for product_data in products_data:
    product, created = Product.objects.get_or_create(
        name=product_data['name'],
        defaults={'price': product_data['price'], 'stock': product_data['stock']}
    )
    status = "Created" if created else "Already exists"
    print(f"{product.name}: {status}")

print("\nAll products ready!")
