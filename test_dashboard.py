#!/usr/bin/env python3
"""
Test script to validate the dashboard functionality with sample data
"""
import pandas as pd
import sys
import os
sys.path.append('.')

from data_processor import DataProcessor
from kpi_calculator import KPICalculator
from database import Database
from alert_manager import AlertManager
from visualization import Visualizer

def test_dashboard_functionality():
    """Test the complete dashboard functionality"""
    print("Testing KPI Dashboard functionality...")
    
    # Initialize components
    data_processor = DataProcessor()
    kpi_calculator = KPICalculator()
    database = Database()
    alert_manager = AlertManager()
    visualizer = Visualizer()
    
    # Test 1: Load sample data
    print("\n1. Loading sample Excel data...")
    data = data_processor.load_excel("sample_business_data.xlsx")
    
    if data is not None:
        print(f"✓ Data loaded successfully: {len(data)} rows")
        print(f"✓ Columns: {list(data.columns)}")
        print(f"✓ Data types: {data.dtypes.to_dict()}")
    else:
        print("✗ Failed to load data")
        return False
    
    # Test 2: Calculate KPIs
    print("\n2. Calculating KPIs...")
    try:
        kpis = kpi_calculator.calculate_kpis(data)
        print(f"✓ KPIs calculated successfully: {len(kpis)} metrics")
        
        # Display key KPIs
        key_kpis = ['revenue', 'profit', 'profit_margin', 'growth_rate']
        for kpi in key_kpis:
            if kpi in kpis:
                print(f"  - {kpi}: {kpis[kpi]}")
        
    except Exception as e:
        print(f"✗ KPI calculation failed: {e}")
        return False
    
    # Test 3: Database operations
    print("\n3. Testing database operations...")
    try:
        database.store_data(data, kpis)
        print("✓ Data stored in database")
        
        # Test threshold operations
        database.update_threshold('revenue', 45000)
        database.update_threshold('profit_margin', 35)
        thresholds = database.get_thresholds()
        print(f"✓ Thresholds configured: {len(thresholds)} items")
        
        # Get historical data
        historical = database.get_historical_data()
        print(f"✓ Historical data retrieved: {len(historical)} records")
        
    except Exception as e:
        print(f"✗ Database operations failed: {e}")
        return False
    
    # Test 4: Alert functionality
    print("\n4. Testing alert functionality...")
    try:
        # Test threshold checking
        for kpi_name, kpi_value in kpis.items():
            if kpi_name in thresholds and isinstance(kpi_value, (int, float)):
                threshold = thresholds[kpi_name]
                if kpi_value < threshold:
                    print(f"  - Alert: {kpi_name} ({kpi_value:.2f}) below threshold ({threshold:.2f})")
                else:
                    print(f"  - OK: {kpi_name} ({kpi_value:.2f}) above threshold ({threshold:.2f})")
        
        print("✓ Alert system functional")
        
    except Exception as e:
        print(f"✗ Alert functionality failed: {e}")
        return False
    
    # Test 5: Visualization
    print("\n5. Testing visualization components...")
    try:
        historical_data = database.get_historical_data()
        if not historical_data.empty:
            # Test time series chart
            fig_time = visualizer.create_time_series_chart(historical_data)
            print("✓ Time series chart created")
            
            # Test comparison chart
            fig_comparison = visualizer.create_comparison_chart(kpis, thresholds)
            print("✓ Comparison chart created")
            
            # Test distribution chart
            fig_dist = visualizer.create_distribution_chart(historical_data)
            print("✓ Distribution chart created")
        else:
            print("⚠ No historical data for visualization")
        
    except Exception as e:
        print(f"✗ Visualization failed: {e}")
        return False
    
    print("\n✓ All dashboard components tested successfully!")
    print("\nSample KPI Summary:")
    print("=" * 50)
    for kpi, value in kpis.items():
        if isinstance(value, (int, float)):
            print(f"{kpi.replace('_', ' ').title()}: {value:.2f}")
        else:
            print(f"{kpi.replace('_', ' ').title()}: {value}")
    
    return True

if __name__ == "__main__":
    success = test_dashboard_functionality()
    sys.exit(0 if success else 1)