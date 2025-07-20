import pandas as pd
import numpy as np
from datetime import datetime
import streamlit as st
from llm_data_extractor import LLMDataExtractor

class DataProcessor:
    def __init__(self):
        self.supported_formats = ['.xlsx', '.xls']
        self.llm_extractor = LLMDataExtractor()
        self.use_llm = True
    
    def load_excel(self, file_path):
        """Load and process Excel file with LLM enhancement"""
        try:
            # Read Excel file
            df = pd.read_excel(file_path)
            
            if self.use_llm and df is not None and not df.empty:
                # Use LLM to extract and standardize data
                st.info("🤖 Using AI to analyze and extract business data...")
                analysis = self.llm_extractor.analyze_excel_structure(df)
                standardized_df = self.llm_extractor.extract_business_data(df)
                
                # Store analysis results for display
                self.last_analysis = analysis
                
                # Display analysis results
                confidence = analysis.get('confidence_score', 0)
                if confidence > 0.7:
                    st.success(f"✅ Data analyzed successfully (Confidence: {confidence:.0%})")
                else:
                    st.warning(f"⚠️ Data analysis completed with lower confidence ({confidence:.0%})")
                
                # Show column mappings
                mappings = analysis.get('column_mappings', {})
                if mappings:
                    st.info("📊 Column mappings identified:")
                    for standard_name, actual_column in mappings.items():
                        if actual_column:
                            st.write(f"• {standard_name.replace('_', ' ').title()}: {actual_column}")
                
                if not standardized_df.empty:
                    return standardized_df
                else:
                    st.warning("LLM extraction returned empty data, falling back to traditional processing")
                    return self.fallback_processing(df)
            else:
                # Traditional processing
                return self.fallback_processing(df)
                
        except Exception as e:
            st.error(f"Error loading Excel file: {str(e)}")
            return None
    
    def fallback_processing(self, df):
        """Traditional data processing when LLM fails"""
        # Basic data cleaning
        df = self.clean_data(df)
        
        # Validate required columns
        if self.validate_data(df):
            return df
        else:
            st.error("Excel file must contain required columns: Date, Revenue, COGS")
            return None
    
    def get_llm_insights(self, df, kpis):
        """Get LLM-generated business insights"""
        if self.use_llm and hasattr(self, 'llm_extractor'):
            try:
                return self.llm_extractor.generate_data_insights(df, kpis)
            except Exception as e:
                st.error(f"Error generating insights: {str(e)}")
                return None
        return None
    
    def get_suggested_thresholds(self, df, kpis):
        """Get LLM-suggested KPI thresholds"""
        if self.use_llm and hasattr(self, 'llm_extractor'):
            try:
                return self.llm_extractor.suggest_kpi_thresholds(df, kpis)
            except Exception as e:
                st.error(f"Error suggesting thresholds: {str(e)}")
                return None
        return None
    
    def clean_data(self, df):
        """Clean and standardize the data"""
        # Convert column names to lowercase and remove spaces
        df.columns = df.columns.str.lower().str.replace(' ', '_')
        
        # Try to identify date column
        date_columns = ['date', 'datetime', 'timestamp', 'time']
        date_col = None
        for col in date_columns:
            if col in df.columns:
                date_col = col
                break
        
        if date_col:
            # Convert to datetime
            df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
            df = df.dropna(subset=[date_col])
            df = df.sort_values(date_col)
        
        # Clean numeric columns
        numeric_columns = ['revenue', 'cogs', 'cost_of_goods_sold', 'sales', 'profit', 'expenses']
        for col in df.columns:
            if any(keyword in col.lower() for keyword in numeric_columns):
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Remove rows with all NaN values
        df = df.dropna(how='all')
        
        return df
    
    def validate_data(self, df):
        """Validate that the data contains required columns"""
        required_columns = ['revenue', 'cogs']
        
        # Check for alternative column names
        column_mapping = {
            'revenue': ['revenue', 'sales', 'total_sales', 'income'],
            'cogs': ['cogs', 'cost_of_goods_sold', 'cost_of_sales', 'costs']
        }
        
        found_columns = {}
        for required_col in required_columns:
            for col in df.columns:
                if any(keyword in col.lower() for keyword in column_mapping[required_col]):
                    found_columns[required_col] = col
                    break
        
        # Rename columns to standard names
        if len(found_columns) >= 2:
            df.rename(columns=found_columns, inplace=True)
            return True
        
        return False
    
    def get_latest_data(self, df, days=30):
        """Get the most recent data within specified days"""
        if 'date' in df.columns:
            cutoff_date = datetime.now() - pd.Timedelta(days=days)
            return df[df['date'] >= cutoff_date]
        return df.tail(days)  # Fallback to last N rows
    
    def calculate_moving_averages(self, df, window=7):
        """Calculate moving averages for key metrics"""
        if 'revenue' in df.columns:
            df['revenue_ma'] = df['revenue'].rolling(window=window).mean()
        
        if 'profit' in df.columns:
            df['profit_ma'] = df['profit'].rolling(window=window).mean()
        
        return df
    
    def detect_anomalies(self, df, column='revenue', threshold=2):
        """Detect anomalies in the data using z-score"""
        if column in df.columns:
            z_scores = np.abs((df[column] - df[column].mean()) / df[column].std())
            df[f'{column}_anomaly'] = z_scores > threshold
        
        return df
    
    def aggregate_data(self, df, period='daily'):
        """Aggregate data by specified period"""
        if 'date' not in df.columns:
            return df
        
        # Set date as index
        df_agg = df.set_index('date')
        
        # Define aggregation rules
        agg_rules = {
            'revenue': 'sum',
            'cogs': 'sum',
            'profit': 'sum'
        }
        
        # Filter only existing columns
        agg_rules = {k: v for k, v in agg_rules.items() if k in df_agg.columns}
        
        if period == 'daily':
            return df_agg.resample('D').agg(agg_rules).reset_index()
        elif period == 'weekly':
            return df_agg.resample('W').agg(agg_rules).reset_index()
        elif period == 'monthly':
            return df_agg.resample('M').agg(agg_rules).reset_index()
        
        return df
