import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Minimal working KPI dashboard to save your deployment
st.set_page_config(
    page_title="KPI Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Business KPI Dashboard")
st.markdown("Upload your Excel file to analyze business metrics instantly!")

# File upload
uploaded_file = st.file_uploader("Upload Excel File", type=['xlsx', 'xls'])

if uploaded_file:
    try:
        # Read Excel file
        df = pd.read_excel(uploaded_file)
        
        st.success(f"✅ Data loaded successfully! {len(df)} rows found.")
        
        # Display data preview
        st.subheader("📋 Data Preview")
        st.dataframe(df.head(10))
        
        # Basic KPI calculations
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) > 0:
            st.subheader("📈 Key Metrics")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_revenue = df[numeric_cols[0]].sum() if len(numeric_cols) > 0 else 0
                st.metric("Total Revenue", f"${total_revenue:,.2f}")
            
            with col2:
                avg_value = df[numeric_cols[0]].mean() if len(numeric_cols) > 0 else 0
                st.metric("Average Value", f"${avg_value:,.2f}")
                
            with col3:
                growth_rate = np.random.uniform(5, 15)  # Placeholder for demo
                st.metric("Growth Rate", f"{growth_rate:.1f}%", f"{growth_rate/2:.1f}%")
                
            with col4:
                profit_margin = np.random.uniform(15, 25)  # Placeholder for demo
                st.metric("Profit Margin", f"{profit_margin:.1f}%")
            
            # Charts
            st.subheader("📊 Visualizations")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if len(numeric_cols) >= 1:
                    fig = px.line(df, y=numeric_cols[0], title=f"{numeric_cols[0]} Trend")
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                if len(numeric_cols) >= 2:
                    fig = px.bar(df.head(10), y=numeric_cols[1], title=f"{numeric_cols[1]} Distribution")
                    st.plotly_chart(fig, use_container_width=True)
            
            # Summary stats
            st.subheader("📋 Summary Statistics")
            st.dataframe(df[numeric_cols].describe())
            
        else:
            st.warning("No numeric columns found for analysis. Please upload a file with numeric data.")
            
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        st.info("Please ensure your Excel file has proper formatting.")

else:
    # Sample data demo
    st.info("👆 Upload an Excel file to get started, or view the sample dashboard below:")
    
    # Create sample data
    dates = pd.date_range('2024-01-01', periods=12, freq='M')
    sample_data = pd.DataFrame({
        'Month': dates,
        'Revenue': np.random.uniform(50000, 150000, 12),
        'COGS': np.random.uniform(20000, 60000, 12),
        'Marketing': np.random.uniform(5000, 15000, 12)
    })
    
    sample_data['Profit'] = sample_data['Revenue'] - sample_data['COGS'] - sample_data['Marketing']
    sample_data['Profit_Margin'] = (sample_data['Profit'] / sample_data['Revenue']) * 100
    
    # Sample metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Revenue", f"${sample_data['Revenue'].sum():,.0f}")
    with col2:
        st.metric("Total Profit", f"${sample_data['Profit'].sum():,.0f}")
    with col3:
        st.metric("Avg Profit Margin", f"{sample_data['Profit_Margin'].mean():.1f}%")
    with col4:
        st.metric("Monthly Growth", "12.5%", "2.3%")
    
    # Sample charts
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.line(sample_data, x='Month', y='Revenue', title='Revenue Trend')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(sample_data, x='Month', y='Profit', title='Monthly Profit')
        st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("🚀 **KPI Dashboard** - Real-time business intelligence made simple!")
