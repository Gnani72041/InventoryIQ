from django.contrib import admin
from .models import Product, SalesRecord, ForecastResult

admin.site.register(Product)
admin.site.register(SalesRecord)
admin.site.register(ForecastResult)