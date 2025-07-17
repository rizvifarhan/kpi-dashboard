import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class KPICalculator:
    def __init__(self):
        self.kpi_definitions = {
            'revenue': 'Total revenue/sales',
            'cogs': 'Cost of goods sold',
            'profit': 'Revenue - COGS',
            'profit_margin': '(Profit / Revenue) * 100',
            'growth_rate': 'Period-over-period growth',
            'revenue_per_day': 'Average daily revenue',
            'efficiency_ratio': 'Revenue / COGS ratio'
        }
    
    def calculate_kpis(self, data):
        """Calculate all KPIs from the data"""
        kpis = {}
        
        if data.empty:
            return kpis
        
        # Basic KPIs - ensure all values are numeric
        kpis['revenue'] = float(self.calculate_revenue(data))
        kpis['cogs'] = float(self.calculate_cogs(data))
        kpis['profit'] = float(self.calculate_profit(data))
        kpis['profit_margin'] = float(self.calculate_profit_margin(data))
        kpis['growth_rate'] = float(self.calculate_growth_rate(data))
        kpis['revenue_per_day'] = float(self.calculate_revenue_per_day(data))
        kpis['efficiency_ratio'] = float(self.calculate_efficiency_ratio(data))
        
        # Trend analysis
        trends = self.calculate_trends(data)
        for key, value in trends.items():
            if isinstance(value, (int, float)):
                kpis[key] = float(value)
            else:
                kpis[key] = value  # Keep string values like 'increasing', 'decreasing'
        
        # Performance metrics
        metrics = self.calculate_performance_metrics(data)
        for key, value in metrics.items():
            if isinstance(value, (int, float)) and not pd.isna(value):
                kpis[key] = float(value)
            else:
                kpis[key] = 0.0  # Default to 0 for NaN values
        
        return kpis
    
    def calculate_revenue(self, data):
        """Calculate total revenue"""
        if 'revenue' in data.columns:
            return data['revenue'].sum()
        return 0
    
    def calculate_cogs(self, data):
        """Calculate total cost of goods sold"""
        if 'cogs' in data.columns:
            return data['cogs'].sum()
        return 0
    
    def calculate_profit(self, data):
        """Calculate total profit"""
        revenue = self.calculate_revenue(data)
        cogs = self.calculate_cogs(data)
        return revenue - cogs
    
    def calculate_profit_margin(self, data):
        """Calculate profit margin percentage"""
        revenue = self.calculate_revenue(data)
        profit = self.calculate_profit(data)
        
        if revenue > 0:
            return (profit / revenue) * 100
        return 0
    
    def calculate_growth_rate(self, data):
        """Calculate growth rate compared to previous period"""
        if 'revenue' not in data.columns or len(data) < 2:
            return 0
        
        # Sort by date if available
        if 'date' in data.columns:
            data = data.sort_values('date')
        
        # Calculate period-over-period growth
        current_period = data.tail(len(data) // 2)['revenue'].sum()
        previous_period = data.head(len(data) // 2)['revenue'].sum()
        
        if previous_period > 0:
            return ((current_period - previous_period) / previous_period) * 100
        return 0
    
    def calculate_revenue_per_day(self, data):
        """Calculate average daily revenue"""
        if 'revenue' not in data.columns:
            return 0
        
        if 'date' in data.columns:
            # Group by date and calculate average
            daily_revenue = data.groupby('date')['revenue'].sum()
            return daily_revenue.mean()
        else:
            # If no date column, assume each row is a day
            return data['revenue'].mean()
    
    def calculate_efficiency_ratio(self, data):
        """Calculate revenue to COGS ratio"""
        revenue = self.calculate_revenue(data)
        cogs = self.calculate_cogs(data)
        
        if cogs > 0:
            return revenue / cogs
        return 0
    
    def calculate_trends(self, data):
        """Calculate trend indicators"""
        trends = {}
        
        if 'revenue' in data.columns and len(data) >= 3:
            # Revenue trend
            revenue_values = data['revenue'].values
            if len(revenue_values) >= 2:
                recent_trend = np.polyfit(range(len(revenue_values)), revenue_values, 1)[0]
                trends['revenue_trend'] = 'increasing' if recent_trend > 0 else 'decreasing'
                trends['revenue_change'] = recent_trend
        
        if 'profit' in data.columns and len(data) >= 3:
            # Profit trend
            profit_values = [self.calculate_profit(data.iloc[i:i+1]) for i in range(len(data))]
            if len(profit_values) >= 2:
                profit_trend = np.polyfit(range(len(profit_values)), profit_values, 1)[0]
                trends['profit_trend'] = 'increasing' if profit_trend > 0 else 'decreasing'
                trends['profit_change'] = profit_trend
        
        return trends
    
    def calculate_performance_metrics(self, data):
        """Calculate additional performance metrics"""
        metrics = {}
        
        if 'revenue' in data.columns:
            # Revenue statistics
            revenue_data = data['revenue']
            metrics['revenue_volatility'] = revenue_data.std()
            metrics['revenue_max'] = revenue_data.max()
            metrics['revenue_min'] = revenue_data.min()
            metrics['revenue_median'] = revenue_data.median()
        
        if 'cogs' in data.columns:
            # Cost statistics
            cogs_data = data['cogs']
            metrics['cogs_volatility'] = cogs_data.std()
            metrics['avg_cogs'] = cogs_data.mean()
        
        # Calculate moving averages if enough data
        if len(data) >= 7:
            metrics.update(self.calculate_moving_averages(data))
        
        return metrics
    
    def calculate_moving_averages(self, data, windows=[7, 14, 30]):
        """Calculate moving averages for different time windows"""
        ma_metrics = {}
        
        for window in windows:
            if len(data) >= window:
                if 'revenue' in data.columns:
                    ma_metrics[f'revenue_ma_{window}'] = data['revenue'].rolling(window=window).mean().iloc[-1]
                
                if 'profit' in data.columns:
                    profit_series = data['revenue'] - data['cogs'] if 'cogs' in data.columns else data['revenue']
                    ma_metrics[f'profit_ma_{window}'] = profit_series.rolling(window=window).mean().iloc[-1]
        
        return ma_metrics
    
    def calculate_seasonal_metrics(self, data):
        """Calculate seasonal performance metrics"""
        if 'date' not in data.columns:
            return {}
        
        data['month'] = pd.to_datetime(data['date']).dt.month
        data['quarter'] = pd.to_datetime(data['date']).dt.quarter
        data['day_of_week'] = pd.to_datetime(data['date']).dt.dayofweek
        
        seasonal_metrics = {}
        
        if 'revenue' in data.columns:
            # Monthly performance
            monthly_revenue = data.groupby('month')['revenue'].mean()
            seasonal_metrics['best_month'] = monthly_revenue.idxmax()
            seasonal_metrics['worst_month'] = monthly_revenue.idxmin()
            
            # Quarterly performance
            quarterly_revenue = data.groupby('quarter')['revenue'].mean()
            seasonal_metrics['best_quarter'] = quarterly_revenue.idxmax()
            
            # Day of week performance
            daily_revenue = data.groupby('day_of_week')['revenue'].mean()
            seasonal_metrics['best_day'] = daily_revenue.idxmax()
        
        return seasonal_metrics
    
    def get_kpi_status(self, kpi_name, current_value, threshold):
        """Get status of KPI compared to threshold"""
        if current_value >= threshold:
            return "good"
        elif current_value >= threshold * 0.9:
            return "warning"
        else:
            return "critical"
    
    def calculate_forecast(self, data, periods=7):
        """Simple forecast using linear regression"""
        if 'revenue' not in data.columns or len(data) < 3:
            return []
        
        # Use simple linear regression for forecasting
        x = np.arange(len(data))
        y = data['revenue'].values
        
        # Calculate trend
        coefficients = np.polyfit(x, y, 1)
        
        # Generate forecast
        forecast = []
        for i in range(periods):
            predicted_value = coefficients[0] * (len(data) + i) + coefficients[1]
            forecast.append(max(0, predicted_value))  # Ensure non-negative
        
        return forecast
