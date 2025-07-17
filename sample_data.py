import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Create sample business data
def create_sample_data():
    # Generate dates for the last 30 days
    dates = [datetime.now() - timedelta(days=i) for i in range(30, 0, -1)]
    
    # Generate sample business data
    np.random.seed(42)
    
    data = {
        'Date': dates,
        'Revenue': np.random.normal(50000, 10000, 30).round(2),
        'COGS': np.random.normal(30000, 5000, 30).round(2),
        'Expenses': np.random.normal(8000, 2000, 30).round(2),
        'Marketing_Spend': np.random.normal(5000, 1000, 30).round(2),
        'Units_Sold': np.random.randint(100, 500, 30),
        'Customer_Acquisition': np.random.randint(10, 50, 30)
    }
    
    # Ensure positive values
    for key in ['Revenue', 'COGS', 'Expenses', 'Marketing_Spend']:
        data[key] = np.maximum(data[key], 1000)
    
    df = pd.DataFrame(data)
    
    # Save to Excel
    df.to_excel('sample_business_data.xlsx', index=False)
    print("Sample data created: sample_business_data.xlsx")
    return df

if __name__ == "__main__":
    df = create_sample_data()
    print(df.head())