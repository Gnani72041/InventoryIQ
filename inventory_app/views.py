from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from .models import Product, SalesRecord, ForecastResult
from .forecast import forecast_demand
from .forms import ProductForm, SalesRecordForm

@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'inventory_app/product_list.html', {'products': products})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'inventory_app/add_product.html', {'form': form})

@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    sales_history = SalesRecord.objects.filter(product=product).order_by('sale_date')
    
    # Generate forecast if we have enough data
    forecast_data = None
    if sales_history.count() >= 7:
        forecast_data = forecast_demand(product, sales_history)
        
        # Save forecast to database
        for forecast in forecast_data:
            ForecastResult.objects.update_or_create(
                product=product,
                forecast_date=forecast['date'],
                defaults={
                    'predicted_demand': forecast['predicted_demand'],
                    'confidence_interval_low': forecast['confidence_low'],
                    'confidence_interval_high': forecast['confidence_high']
                }
            )
    
    # Check stock status
    stock_status = "adequate"
    if product.current_stock < product.min_stock_level:
        stock_status = "low"
    elif forecast_data and product.current_stock < forecast_data[0]['predicted_demand']:
        stock_status = "risk"
    
    return render(request, 'inventory_app/product_detail.html', {
        'product': product,
        'sales_history': sales_history,
        'forecast_data': forecast_data,
        'stock_status': stock_status
    })

@login_required
def add_sale(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = SalesRecordForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.product = product
            sale.save()
            
            # Update product stock
            product.current_stock -= sale.quantity_sold
            product.save()

            # 🔹 Recalculate forecast after new sale
            sales_history = SalesRecord.objects.filter(product=product).order_by('sale_date')
            if sales_history.count() >= 7:
                forecast_data = forecast_demand(product, sales_history)
                for forecast in forecast_data:
                    ForecastResult.objects.update_or_create(
                        product=product,
                        forecast_date=forecast['date'],
                        defaults={
                            'predicted_demand': forecast['predicted_demand'],
                            'confidence_interval_low': forecast['confidence_low'],
                            'confidence_interval_high': forecast['confidence_high']
                        }
                    )

            messages.success(request, 'Sale recorded successfully!')
            return redirect('product_detail', product_id=product_id)
    else:
        form = SalesRecordForm()
    return render(request, 'inventory_app/add_sale.html', {'form': form, 'product': product})


@login_required
def dashboard(request):
    products = Product.objects.all()
    low_stock_products = products.filter(current_stock__lt=models.F('min_stock_level'))

    forecast_data = []
    for product in products:
        # Get sales history
        sales_history = SalesRecord.objects.filter(product=product).order_by('sale_date')

        if sales_history.count() >= 7:
            # Check if forecast exists in DB
            forecasts = ForecastResult.objects.filter(product=product).order_by('forecast_date')

            if not forecasts.exists():
                # 🔹 Generate forecast if not found in DB
                forecast_list = forecast_demand(product, sales_history)
                if forecast_list:
                    for forecast in forecast_list:
                        ForecastResult.objects.update_or_create(
                            product=product,
                            forecast_date=forecast['date'],
                            defaults={
                                'predicted_demand': forecast['predicted_demand'],
                                'confidence_interval_low': forecast['confidence_low'],
                                'confidence_interval_high': forecast['confidence_high']
                            }
                        )
                    forecasts = ForecastResult.objects.filter(product=product).order_by('forecast_date')

            # If forecasts exist now, calculate average demand
            if forecasts.exists():
                avg_predicted = sum(f.predicted_demand for f in forecasts) // forecasts.count()
                forecast_data.append({
                    'product': product.name,
                    'predicted_demand': avg_predicted,
                    'current_stock': product.current_stock,
                    'status': 'low' if product.current_stock < avg_predicted else 'adequate'
                })
            else:
                # No forecast generated, fallback
                forecast_data.append({
                    'product': product.name,
                    'predicted_demand': 'N/A',
                    'current_stock': product.current_stock,
                    'status': 'low' if product.current_stock < product.min_stock_level else 'adequate'
                })
        else:
            # Not enough sales to generate forecast
            forecast_data.append({
                'product': product.name,
                'predicted_demand': 'N/A',
                'current_stock': product.current_stock,
                'status': 'low' if product.current_stock < product.min_stock_level else 'adequate'
            })

    return render(request, 'inventory_app/dashboard.html', {
        'total_products': products.count(),
        'low_stock_products': low_stock_products,
        'forecast_data': forecast_data
    })
