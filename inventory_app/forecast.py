import pandas as pd
from datetime import datetime, timedelta

def forecast_demand(product, sales_history):
    """Generate simple demand forecast for a product"""
    try:
        # Convert to list first, then DataFrame
        sales_list = list(sales_history.values('sale_date', 'quantity_sold'))
        if not sales_list or len(sales_list) < 7:
            return None
            
        df = pd.DataFrame(sales_list)
        df['sale_date'] = pd.to_datetime(df['sale_date'])
        df = df.sort_values('sale_date')
        
        # Get last 7 days average
        last_7_days = df.tail(7)['quantity_sold'].mean()
        
        # If no data, return None
        if pd.isna(last_7_days):
            return None
            
        # Forecast next 30 days
        last_date = df['sale_date'].max()
        
        forecasts = []
        for i in range(1, 31):
            date = last_date + timedelta(days=i)
            
            # Simple prediction based on 7-day average
            predicted = round(last_7_days)
            
            forecasts.append({
                'date': date,
                'predicted_demand': predicted,
                'confidence_low': max(1, round(predicted * 0.7)),
                'confidence_high': round(predicted * 1.3)
            })
        
        return forecasts
        
    except Exception as e:
        print(f"Forecasting error for {product.name}: {e}")
        return None