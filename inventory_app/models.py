from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    current_stock = models.IntegerField(default=0)
    min_stock_level = models.IntegerField(default=10)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class SalesRecord(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_sold = models.IntegerField()
    sale_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.product.name} - {self.quantity_sold} on {self.sale_date}"

class ForecastResult(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    forecast_date = models.DateField()
    predicted_demand = models.IntegerField()
    confidence_interval_low = models.IntegerField()
    confidence_interval_high = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.product.name} forecast on {self.forecast_date}"