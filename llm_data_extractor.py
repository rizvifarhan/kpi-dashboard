import os
import json
import pandas as pd
from openai import OpenAI
from typing import Dict, Any, List, Optional

class LLMDataExtractor:
    def __init__(self):
        api_key = os.environ.get("OPENROUTER_API_KEY")
        if api_key:
            self.client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key
            )
            self.model = "qwen/qwen-2.5-3b-instruct"
            self.enabled = True
        else:
            self.client = None
            self.enabled = False
    
    def analyze_excel_structure(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Use LLM to analyze Excel structure and identify business data columns
        """
        if not self.enabled or not self.client:
            return self._fallback_analysis(df)
        
        # Get first few rows as sample
        sample_data = df.head(10).to_string()
        column_names = list(df.columns)
        
        prompt = f"""
        Analyze this Excel data and identify business metrics columns. Return a JSON response with column mappings.
        
        Column names: {column_names}
        Sample data:
        {sample_data}
        
        Please identify and map the following business metrics to actual column names:
        - date: Column containing dates/timestamps
        - revenue: Total revenue/sales/income
        - cogs: Cost of goods sold/cost of sales/expenses
        - profit: Net profit/earnings (if available)
        - units_sold: Number of units/items sold (if available)
        - customers: Number of customers/clients (if available)
        
        Return JSON in this exact format:
        {{
            "column_mappings": {{
                "date": "actual_column_name_or_null",
                "revenue": "actual_column_name_or_null",
                "cogs": "actual_column_name_or_null",
                "profit": "actual_column_name_or_null",
                "units_sold": "actual_column_name_or_null",
                "customers": "actual_column_name_or_null"
            }},
            "data_quality": {{
                "has_date_column": true_or_false,
                "has_revenue_data": true_or_false,
                "data_completeness": "percentage_string",
                "suggested_processing": "brief_suggestion"
            }},
            "confidence_score": 0.95
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert data analyst. Analyze Excel data and identify business metrics columns. Always respond with valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content
            if content:
                result = json.loads(content)
                return result
            else:
                return self._fallback_analysis(df)
            
        except Exception as e:
            print(f"LLM analysis error: {e}")
            return self._fallback_analysis(df)
    
    def extract_business_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract and standardize business data using LLM insights
        """
        # Get LLM analysis
        analysis = self.analyze_excel_structure(df)
        column_mappings = analysis.get("column_mappings", {})
        
        # Create standardized dataframe
        standardized_df = pd.DataFrame()
        
        # Map columns based on LLM analysis
        for standard_name, actual_column in column_mappings.items():
            if actual_column and actual_column in df.columns:
                standardized_df[standard_name] = df[actual_column]
        
        # Ensure we have required columns
        if 'date' not in standardized_df.columns:
            # Try to find date column manually
            date_column = self._find_date_column(df)
            if date_column:
                standardized_df['date'] = df[date_column]
        
        if 'revenue' not in standardized_df.columns:
            # Try to find revenue column manually
            revenue_column = self._find_revenue_column(df)
            if revenue_column:
                standardized_df['revenue'] = df[revenue_column]
        
        # Clean and convert data types
        standardized_df = self._clean_extracted_data(standardized_df)
        
        return standardized_df
    
    def generate_data_insights(self, df: pd.DataFrame, kpis: Dict[str, Any]) -> str:
        """
        Generate business insights using LLM
        """
        if not self.enabled or not self.client:
            return "AI insights are not available. Please configure OpenRouter API key."
        # Create summary of the data
        data_summary = {
            "total_records": len(df),
            "date_range": f"{df['date'].min()} to {df['date'].max()}" if 'date' in df.columns else "Unknown",
            "total_revenue": kpis.get('total_revenue', 0),
            "avg_profit_margin": kpis.get('avg_profit_margin', 0),
            "growth_rate": kpis.get('growth_rate', 0)
        }
        
        prompt = f"""
        Based on this business data analysis, provide actionable insights and recommendations:
        
        Data Summary:
        {json.dumps(data_summary, indent=2)}
        
        Key Performance Indicators:
        {json.dumps(kpis, indent=2)}
        
        Please provide:
        1. Key business insights (3-4 bullet points)
        2. Performance trends
        3. Actionable recommendations
        4. Potential areas of concern
        
        Keep the response concise and business-focused.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a business analyst providing insights based on KPI data. Be concise and actionable."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=800
            )
            
            content = response.choices[0].message.content
            return content if content else "Unable to generate insights at this time."
            
        except Exception as e:
            print(f"Insight generation error: {e}")
            return "Unable to generate insights at this time."
    
    def suggest_kpi_thresholds(self, df: pd.DataFrame, kpis: Dict[str, Any]) -> Dict[str, float]:
        """
        Suggest appropriate KPI thresholds based on historical data
        """
        if not self.enabled or not self.client:
            # Provide intelligent fallback thresholds based on actual data
            revenue = kpis.get('revenue', kpis.get('total_revenue', 0))
            profit_margin = kpis.get('profit_margin', kpis.get('avg_profit_margin', 0))
            
            return {
                "revenue_threshold": max(revenue * 0.8, 10000) if revenue > 0 else 50000,
                "profit_margin_threshold": max(profit_margin * 0.9, 15.0) if profit_margin > 0 else 20.0,
                "growth_rate_threshold": 2.0  # Reasonable default growth target
            }
        # Calculate basic statistics
        stats = {}
        if 'revenue' in df.columns:
            stats['revenue_mean'] = df['revenue'].mean()
            stats['revenue_std'] = df['revenue'].std()
        
        prompt = f"""
        Based on this business data, suggest appropriate alert thresholds for KPIs:
        
        Historical Data Stats:
        {json.dumps(stats, indent=2)}
        
        Current KPIs:
        {json.dumps(kpis, indent=2)}
        
        Suggest thresholds for:
        - revenue_threshold: Minimum acceptable revenue
        - profit_margin_threshold: Minimum acceptable profit margin (%)
        - growth_rate_threshold: Minimum acceptable growth rate (%)
        
        Return JSON format:
        {{
            "revenue_threshold": number,
            "profit_margin_threshold": number,
            "growth_rate_threshold": number
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a business analyst. Suggest realistic KPI thresholds based on historical data. Return valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=300
            )
            
            content = response.choices[0].message.content
            if content:
                result = json.loads(content)
                return result
            else:
                return {
                    "revenue_threshold": kpis.get('total_revenue', 0) * 0.8,
                    "profit_margin_threshold": 10.0,
                    "growth_rate_threshold": 0.0
                }
            
        except Exception as e:
            print(f"Threshold suggestion error: {e}")
            # Intelligent fallback thresholds
            revenue = kpis.get('revenue', kpis.get('total_revenue', 0))
            profit_margin = kpis.get('profit_margin', kpis.get('avg_profit_margin', 0))
            
            return {
                "revenue_threshold": max(revenue * 0.8, 10000) if revenue > 0 else 50000,
                "profit_margin_threshold": max(profit_margin * 0.9, 15.0) if profit_margin > 0 else 20.0,
                "growth_rate_threshold": 2.0
            }
    
    def _fallback_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Fallback analysis when LLM fails
        """
        columns = df.columns.str.lower()
        
        # Try to identify columns manually
        date_col = None
        revenue_col = None
        cogs_col = None
        
        for col in df.columns:
            col_lower = col.lower()
            if any(word in col_lower for word in ['date', 'time', 'period']):
                date_col = col
            elif any(word in col_lower for word in ['revenue', 'sales', 'income']):
                revenue_col = col
            elif any(word in col_lower for word in ['cogs', 'cost', 'expense']):
                cogs_col = col
        
        return {
            "column_mappings": {
                "date": date_col,
                "revenue": revenue_col,
                "cogs": cogs_col,
                "profit": None,
                "units_sold": None,
                "customers": None
            },
            "data_quality": {
                "has_date_column": date_col is not None,
                "has_revenue_data": revenue_col is not None,
                "data_completeness": "Unknown",
                "suggested_processing": "Manual column mapping recommended"
            },
            "confidence_score": 0.5
        }
    
    def _find_date_column(self, df: pd.DataFrame) -> Optional[str]:
        """Find date column manually"""
        for col in df.columns:
            if any(word in col.lower() for word in ['date', 'time', 'period']):
                return col
        return None
    
    def _find_revenue_column(self, df: pd.DataFrame) -> Optional[str]:
        """Find revenue column manually"""
        for col in df.columns:
            if any(word in col.lower() for word in ['revenue', 'sales', 'income']):
                return col
        return None
    
    def _clean_extracted_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and convert extracted data"""
        # Convert date column
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
        
        # Convert numeric columns
        numeric_columns = ['revenue', 'cogs', 'profit', 'units_sold', 'customers']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Remove rows with invalid dates
        if 'date' in df.columns:
            df = df.dropna(subset=['date'])
        
        # Sort by date
        if 'date' in df.columns:
            df = df.sort_values('date')
        
        return df