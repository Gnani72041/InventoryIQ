from django import forms
from .models import Product, SalesRecord

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'sku', 'description', 'current_stock', 'min_stock_level', 'cost_price', 'selling_price']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class SalesRecordForm(forms.ModelForm):
    class Meta:
        model = SalesRecord
        fields = ['quantity_sold', 'sale_date']
        widgets = {
            'sale_date': forms.DateInput(attrs={'type': 'date'}),
        }