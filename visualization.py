import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

class Visualizer:
    def __init__(self):
        self.color_scheme = {
            'primary': '#1f77b4',
            'secondary': '#ff7f0e',
            'success': '#2ca02c',
            'warning': '#d62728',
            'info': '#9467bd',
            'background': '#f8f9fa'
        }
    
    def create_time_series_chart(self, data):
        """Create time series chart for KPI trends"""
        if data.empty:
            return go.Figure()
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Revenue Trend', 'Profit Trend', 'Profit Margin', 'Growth Rate'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Handle x-axis data properly
        if 'timestamp' in data.columns:
            x_axis = pd.to_datetime(data['timestamp']).dt.strftime('%Y-%m-%d')
        elif 'date' in data.columns:
            x_axis = pd.to_datetime(data['date']).dt.strftime('%Y-%m-%d')
        else:
            x_axis = list(range(len(data)))
        
        # Revenue trend
        if 'revenue' in data.columns:
            revenue_data = pd.to_numeric(data['revenue'], errors='coerce').fillna(0)
            fig.add_trace(
                go.Scatter(
                    x=x_axis,
                    y=revenue_data,
                    mode='lines+markers',
                    name='Revenue',
                    line=dict(color=self.color_scheme['primary'])
                ),
                row=1, col=1
            )
        
        # Profit trend
        if 'profit' in data.columns:
            profit_data = pd.to_numeric(data['profit'], errors='coerce').fillna(0)
            fig.add_trace(
                go.Scatter(
                    x=x_axis,
                    y=profit_data,
                    mode='lines+markers',
                    name='Profit',
                    line=dict(color=self.color_scheme['success'])
                ),
                row=1, col=2
            )
        
        # Profit margin
        if 'profit_margin' in data.columns:
            margin_data = pd.to_numeric(data['profit_margin'], errors='coerce').fillna(0)
            fig.add_trace(
                go.Scatter(
                    x=x_axis,
                    y=margin_data,
                    mode='lines+markers',
                    name='Profit Margin (%)',
                    line=dict(color=self.color_scheme['secondary'])
                ),
                row=2, col=1
            )
        
        # Growth rate
        if 'growth_rate' in data.columns:
            growth_data = pd.to_numeric(data['growth_rate'], errors='coerce').fillna(0)
            fig.add_trace(
                go.Scatter(
                    x=x_axis,
                    y=growth_data,
                    mode='lines+markers',
                    name='Growth Rate (%)',
                    line=dict(color=self.color_scheme['info'])
                ),
                row=2, col=2
            )
        
        fig.update_layout(
            title="KPI Trends Over Time",
            height=600,
            showlegend=False
        )
        
        return fig
    
    def create_comparison_chart(self, kpis, thresholds):
        """Create comparison chart of current KPIs vs thresholds"""
        if not kpis:
            return go.Figure()
        
        kpi_names = []
        current_values = []
        threshold_values = []
        colors = []
        
        for kpi_name, current_value in kpis.items():
            if kpi_name in thresholds and isinstance(current_value, (int, float)):
                try:
                    numeric_value = float(current_value)
                    threshold_value = float(thresholds[kpi_name])
                    
                    kpi_names.append(kpi_name.replace('_', ' ').title())
                    current_values.append(numeric_value)
                    threshold_values.append(threshold_value)
                    
                    # Color based on performance
                    if numeric_value >= threshold_value:
                        colors.append(self.color_scheme['success'])
                    elif numeric_value >= threshold_value * 0.9:
                        colors.append(self.color_scheme['warning'])
                    else:
                        colors.append(self.color_scheme['warning'])
                except (ValueError, TypeError):
                    continue
        
        if not kpi_names:
            return go.Figure()
        
        fig = go.Figure()
        
        # Add current values
        fig.add_trace(go.Bar(
            name='Current Value',
            x=kpi_names,
            y=current_values,
            marker_color=colors,
            text=[f'{val:.1f}' for val in current_values],
            textposition='auto'
        ))
        
        # Add threshold lines
        fig.add_trace(go.Scatter(
            name='Threshold',
            x=kpi_names,
            y=threshold_values,
            mode='markers+lines',
            line=dict(color='red', dash='dash'),
            marker=dict(size=8, color='red')
        ))
        
        fig.update_layout(
            title="Current KPIs vs Thresholds",
            xaxis_title="KPI",
            yaxis_title="Value",
            barmode='group',
            height=400
        )
        
        return fig
    
    def create_distribution_chart(self, data):
        """Create distribution chart for KPI values"""
        if data.empty:
            return go.Figure()
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Revenue Distribution', 'Profit Distribution', 
                          'COGS Distribution', 'Profit Margin Distribution'),
            specs=[[{"type": "histogram"}, {"type": "histogram"}],
                   [{"type": "histogram"}, {"type": "histogram"}]]
        )
        
        # Revenue distribution
        if 'revenue' in data.columns:
            revenue_data = pd.to_numeric(data['revenue'], errors='coerce').dropna()
            if not revenue_data.empty:
                fig.add_trace(
                    go.Histogram(
                        x=revenue_data,
                        name='Revenue',
                        nbinsx=20,
                        marker_color=self.color_scheme['primary']
                    ),
                    row=1, col=1
                )
        
        # Profit distribution
        if 'profit' in data.columns:
            profit_data = pd.to_numeric(data['profit'], errors='coerce').dropna()
            if not profit_data.empty:
                fig.add_trace(
                    go.Histogram(
                        x=profit_data,
                        name='Profit',
                        nbinsx=20,
                        marker_color=self.color_scheme['success']
                    ),
                    row=1, col=2
                )
        
        # COGS distribution
        if 'cogs' in data.columns:
            cogs_data = pd.to_numeric(data['cogs'], errors='coerce').dropna()
            if not cogs_data.empty:
                fig.add_trace(
                    go.Histogram(
                        x=cogs_data,
                        name='COGS',
                        nbinsx=20,
                        marker_color=self.color_scheme['warning']
                    ),
                    row=2, col=1
                )
        
        # Profit margin distribution
        if 'profit_margin' in data.columns:
            margin_data = pd.to_numeric(data['profit_margin'], errors='coerce').dropna()
            if not margin_data.empty:
                fig.add_trace(
                    go.Histogram(
                        x=margin_data,
                        name='Profit Margin',
                        nbinsx=20,
                        marker_color=self.color_scheme['secondary']
                    ),
                    row=2, col=2
                )
        
        fig.update_layout(
            title="KPI Distributions",
            height=600,
            showlegend=False
        )
        
        return fig
    
    def create_gauge_chart(self, value, title, min_val=0, max_val=100, threshold=None):
        """Create gauge chart for individual KPI"""
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=value,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': title},
            delta={'reference': threshold if threshold else value * 0.8},
            gauge={
                'axis': {'range': [min_val, max_val]},
                'bar': {'color': self.color_scheme['primary']},
                'steps': [
                    {'range': [min_val, max_val * 0.6], 'color': "lightgray"},
                    {'range': [max_val * 0.6, max_val * 0.8], 'color': "gray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': threshold if threshold else max_val * 0.9
                }
            }
        ))
        
        fig.update_layout(height=300)
        return fig
    
    def create_waterfall_chart(self, categories, values):
        """Create waterfall chart for profit breakdown"""
        fig = go.Figure(go.Waterfall(
            name="Profit Analysis",
            orientation="v",
            measure=["relative", "relative", "total"],
            x=categories,
            textposition="outside",
            text=[f"${val:,.0f}" for val in values],
            y=values,
            connector={"line": {"color": "rgb(63, 63, 63)"}},
        ))
        
        fig.update_layout(
            title="Profit Waterfall Analysis",
            showlegend=False,
            height=400
        )
        
        return fig
    
    def create_heatmap(self, data, title="Performance Heatmap"):
        """Create heatmap for performance analysis"""
        if 'date' not in data.columns:
            return go.Figure()
        
        # Convert date to datetime and extract components
        data['date'] = pd.to_datetime(data['date'])
        data['day'] = data['date'].dt.day
        data['month'] = data['date'].dt.month
        
        # Create pivot table for heatmap
        if 'revenue' in data.columns:
            pivot_data = data.pivot_table(
                values='revenue',
                index='day',
                columns='month',
                aggfunc='sum'
            )
            
            fig = go.Figure(data=go.Heatmap(
                z=pivot_data.values,
                x=pivot_data.columns,
                y=pivot_data.index,
                colorscale='Viridis',
                hoverongaps=False
            ))
            
            fig.update_layout(
                title=title,
                xaxis_title="Month",
                yaxis_title="Day",
                height=400
            )
            
            return fig
        
        return go.Figure()
    
    def create_box_plot(self, data, column='revenue'):
        """Create box plot for data distribution analysis"""
        if column not in data.columns:
            return go.Figure()
        
        fig = go.Figure()
        
        fig.add_trace(go.Box(
            y=data[column],
            name=column.replace('_', ' ').title(),
            boxpoints='outliers',
            marker_color=self.color_scheme['primary']
        ))
        
        fig.update_layout(
            title=f"{column.replace('_', ' ').title()} Distribution Analysis",
            yaxis_title="Value",
            height=400
        )
        
        return fig
    
    def create_correlation_matrix(self, data):
        """Create correlation matrix heatmap"""
        numeric_columns = data.select_dtypes(include=[np.number]).columns
        
        if len(numeric_columns) < 2:
            return go.Figure()
        
        correlation_matrix = data[numeric_columns].corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=correlation_matrix.values,
            x=correlation_matrix.columns,
            y=correlation_matrix.columns,
            colorscale='RdBu',
            zmid=0,
            text=correlation_matrix.values,
            texttemplate='%{text:.2f}',
            textfont={"size": 10}
        ))
        
        fig.update_layout(
            title="KPI Correlation Matrix",
            height=500
        )
        
        return fig
