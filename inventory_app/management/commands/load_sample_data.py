from django.core.management.base import BaseCommand
from inventory_app.models import Product, SalesRecord
import random
from datetime import datetime, timedelta
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Load sample data for testing'

    def handle(self, *args, **options):
        # Create a default user if none exists
        if not User.objects.exists():
            User.objects.create_user('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Created default user: admin/admin123'))
        
        # Create sample products
        products_data = [
            {'name': 'Wireless Mouse', 'sku': 'WM001', 'current_stock': 45, 'min_stock_level': 20},
            {'name': 'Mechanical Keyboard', 'sku': 'MK002', 'current_stock': 32, 'min_stock_level': 15},
            {'name': 'USB-C Cable', 'sku': 'UC003', 'current_stock': 120, 'min_stock_level': 50},
            {'name': 'Laptop Stand', 'sku': 'LS004', 'current_stock': 18, 'min_stock_level': 10},
            {'name': 'Webcam', 'sku': 'WC005', 'current_stock': 25, 'min_stock_level': 12},
        ]
        
        for data in products_data:
            product, created = Product.objects.get_or_create(
                sku=data['sku'],
                defaults={
                    'name': data['name'],
                    'current_stock': data['current_stock'],
                    'min_stock_level': data['min_stock_level'],
                    'cost_price': round(random.uniform(5, 50), 2),
                    'selling_price': round(random.uniform(10, 100), 2),
                    'description': f'Sample {data["name"]} for demonstration'
                }
            )
            
            # Create sales records for the past 90 days
            if created:
                for i in range(90):
                    sale_date = datetime.now().date() - timedelta(days=90-i)
                    quantity = random.randint(1, 10)
                    
                    # Add some seasonality (more sales on weekdays)
                    if sale_date.weekday() < 5:  # Weekday
                        quantity = random.randint(3, 10)
                    else:  # Weekend
                        quantity = random.randint(1, 5)
                    
                    SalesRecord.objects.create(
                        product=product,
                        quantity_sold=quantity,
                        sale_date=sale_date
                    )
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded sample data'))