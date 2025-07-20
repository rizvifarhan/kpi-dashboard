import streamlit as st
import pandas as pd
import time
import os
from datetime import datetime, timedelta
import threading
from data_processor import DataProcessor
from alert_manager import AlertManager
from database import Database
from file_monitor import FileMonitor
from kpi_calculator import KPICalculator
from visualization import Visualizer

# Initialize session state
if 'data_processor' not in st.session_state:
    st.session_state.data_processor = DataProcessor()
if 'alert_manager' not in st.session_state:
    st.session_state.alert_manager = AlertManager()
if 'database' not in st.session_state:
    st.session_state.database = Database()
if 'kpi_calculator' not in st.session_state:
    st.session_state.kpi_calculator = KPICalculator()
if 'visualizer' not in st.session_state:
    st.session_state.visualizer = Visualizer()
if 'file_monitor' not in st.session_state:
    st.session_state.file_monitor = None
if 'last_update' not in st.session_state:
    st.session_state.last_update = None
if 'current_data' not in st.session_state:
    st.session_state.current_data = None
if 'uploaded_file_path' not in st.session_state:
    st.session_state.uploaded_file_path = None

def main():
    st.set_page_config(
        page_title="KPI Dashboard",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("📊 Real-Time Business KPI Dashboard")
    st.markdown("Monitor your business metrics and get automated alerts when thresholds are breached.")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        
        # File upload section
        st.subheader("Data Upload")
        uploaded_file = st.file_uploader(
            "Upload Excel file",
            type=['xlsx', 'xls'],
            help="Upload your business data Excel file"
        )
        
        if uploaded_file is not None:
            # Save uploaded file
            file_path = f"temp_{uploaded_file.name}"
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Process the file if it's new or changed
            if st.session_state.uploaded_file_path != file_path:
                st.session_state.uploaded_file_path = file_path
                process_uploaded_file(file_path)
        
        # Alert configuration
        st.subheader("Alert Settings")
        
        # WhatsApp settings
        st.write("WhatsApp Configuration")
        whatsapp_token = st.text_input("WhatsApp API Token", type="password", value=os.getenv("WHATSAPP_TOKEN", ""))
        whatsapp_phone = st.text_input("WhatsApp Phone Number", value=os.getenv("WHATSAPP_PHONE", ""))
        
        # Slack settings
        st.write("Slack Configuration")
        slack_token = st.text_input("Slack Bot Token", type="password", value=os.getenv("SLACK_TOKEN", ""))
        slack_channel = st.text_input("Slack Channel", value=os.getenv("SLACK_CHANNEL", "#alerts"))
        
        # Update alert manager settings
        st.session_state.alert_manager.configure_whatsapp(whatsapp_token, whatsapp_phone)
        st.session_state.alert_manager.configure_slack(slack_token, slack_channel)
        
        # AI Settings
        st.subheader("🤖 AI Settings")
        use_llm = st.checkbox("Enable AI Data Analysis", value=True, help="Use Qwen3B AI to intelligently extract and analyze business data")
        st.session_state.data_processor.use_llm = use_llm
        
        if use_llm:
            openrouter_key = os.getenv("OPENROUTER_API_KEY")
            if openrouter_key and len(openrouter_key) > 10:
                st.success("✅ AI Analysis Enabled")
                # Test if LLM is actually working
                if hasattr(st.session_state.data_processor.llm_extractor, 'enabled'):
                    if not st.session_state.data_processor.llm_extractor.enabled:
                        st.warning("⚠️ AI Analysis may not be working properly")
            else:
                st.error("❌ OpenRouter API Key Required")
                st.info("Add your OpenRouter API key in the Replit Secrets tab")
        
        # Auto-refresh toggle
        auto_refresh = st.checkbox("Auto-refresh (30 seconds)", value=True)
        
        if st.button("Manual Refresh"):
            if st.session_state.uploaded_file_path:
                process_uploaded_file(st.session_state.uploaded_file_path)
            st.rerun()
    
    # Main dashboard
    if st.session_state.current_data is not None:
        display_dashboard()
    else:
        st.info("Please upload an Excel file to begin monitoring your KPIs.")
        st.markdown("""
        ### Expected Excel Format:
        Your Excel file should contain columns for:
        - Date/Time
        - Revenue
        - Cost of Goods Sold (COGS)
        - Other relevant business metrics
        
        The system will automatically calculate KPIs like profit margins, growth rates, and trends.
        """)
    
    # Auto-refresh mechanism
    if auto_refresh and st.session_state.uploaded_file_path:
        time.sleep(30)
        if os.path.exists(st.session_state.uploaded_file_path):
            # Check if file has been modified
            current_mtime = os.path.getmtime(st.session_state.uploaded_file_path)
            if st.session_state.last_update is None or current_mtime > st.session_state.last_update:
                process_uploaded_file(st.session_state.uploaded_file_path)
                st.rerun()

def process_uploaded_file(file_path):
    """Process the uploaded Excel file and update data"""
    try:
        with st.spinner("Processing Excel file..."):
            # Load and process data
            data = st.session_state.data_processor.load_excel(file_path)
            
            if data is not None and not data.empty:
                # Calculate KPIs
                kpis = st.session_state.kpi_calculator.calculate_kpis(data)
                
                # Store in database
                st.session_state.database.store_data(data, kpis)
                
                # Update session state
                st.session_state.current_data = data
                st.session_state.last_update = time.time()
                
                # Check thresholds and send alerts
                check_thresholds(kpis)
                
                st.success("Data processed successfully!")
            else:
                st.error("Could not process the Excel file. Please check the format.")
                
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")

def check_thresholds(kpis):
    """Check KPI thresholds and send alerts if necessary"""
    thresholds = st.session_state.database.get_thresholds()
    
    for kpi_name, kpi_value in kpis.items():
        if kpi_name in thresholds:
            threshold = thresholds[kpi_name]
            if kpi_value < threshold:
                # Send alert
                alert_message = f"🚨 Alert: {kpi_name} is below threshold!\nCurrent: {kpi_value:.2f}\nThreshold: {threshold:.2f}"
                st.session_state.alert_manager.send_alert(alert_message)

def display_dashboard():
    """Display the main KPI dashboard"""
    data = st.session_state.current_data
    
    if data is None:
        st.warning("No data available")
        return
    
    # Calculate current KPIs
    kpis = st.session_state.kpi_calculator.calculate_kpis(data)
    
    # Display KPI metrics
    st.subheader("Key Performance Indicators")
    
    # Create columns for KPI display
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if 'revenue' in kpis:
            try:
                revenue_val = float(kpis['revenue'])
                revenue_change = float(kpis.get('revenue_change', 0))
                st.metric("Revenue", f"${revenue_val:,.2f}", delta=f"{revenue_change:.1f}%")
            except (ValueError, TypeError):
                st.metric("Revenue", f"${kpis['revenue']}")
    
    with col2:
        if 'profit' in kpis:
            try:
                profit_val = float(kpis['profit'])
                profit_change = float(kpis.get('profit_change', 0))
                st.metric("Profit", f"${profit_val:,.2f}", delta=f"{profit_change:.1f}%")
            except (ValueError, TypeError):
                st.metric("Profit", f"${kpis['profit']}")
    
    with col3:
        if 'profit_margin' in kpis:
            try:
                margin_val = float(kpis['profit_margin'])
                margin_change = float(kpis.get('margin_change', 0))
                st.metric("Profit Margin", f"{margin_val:.1f}%", delta=f"{margin_change:.1f}%")
            except (ValueError, TypeError):
                st.metric("Profit Margin", f"{kpis['profit_margin']}%")
    
    with col4:
        if 'growth_rate' in kpis:
            try:
                growth_val = float(kpis['growth_rate'])
                st.metric("Growth Rate", f"{growth_val:.1f}%")
            except (ValueError, TypeError):
                st.metric("Growth Rate", f"{kpis['growth_rate']}%")
    
    # Threshold configuration
    st.subheader("Threshold Configuration")
    
    # Only show numeric KPIs for threshold configuration
    numeric_kpis = {k: v for k, v in kpis.items() if isinstance(v, (int, float))}
    
    if numeric_kpis:
        threshold_cols = st.columns(len(numeric_kpis))
        thresholds = st.session_state.database.get_thresholds()
        
        for i, (kpi_name, kpi_value) in enumerate(numeric_kpis.items()):
            with threshold_cols[i % len(threshold_cols)]:
                # Ensure kpi_value is numeric
                try:
                    numeric_value = float(kpi_value) if isinstance(kpi_value, (int, float, str)) else 0
                except (ValueError, TypeError):
                    numeric_value = 0
                
                # Get or set default threshold
                default_threshold = max(numeric_value * 0.8, 0) if numeric_value > 0 else 100
                current_threshold = thresholds.get(kpi_name, default_threshold)
                
                new_threshold = st.number_input(
                    f"{kpi_name.replace('_', ' ').title()} Threshold",
                    value=float(current_threshold),
                    min_value=0.0,
                    key=f"threshold_{kpi_name}"
                )
                
                # Color coding based on threshold (only for numeric KPIs)
                if isinstance(numeric_value, (int, float)) and isinstance(new_threshold, (int, float)):
                    if numeric_value < new_threshold:
                        st.error(f"⚠️ Below threshold! (Current: {numeric_value:.2f})")
                    elif numeric_value < new_threshold * 1.1:
                        st.warning(f"⚡ Approaching threshold (Current: {numeric_value:.2f})")
                    else:
                        st.success(f"✅ Above threshold (Current: {numeric_value:.2f})")
                else:
                    st.info(f"Current value: {kpi_value}")
                
                # Update threshold in database
                st.session_state.database.update_threshold(kpi_name, new_threshold)
    else:
        st.info("No numeric KPIs available for threshold configuration.")
    
    # Visualizations
    st.subheader("Trend Analysis")
    
    # Get historical data
    historical_data = st.session_state.database.get_historical_data()
    
    if not historical_data.empty:
        # Create tabs for different chart types
        tab1, tab2, tab3 = st.tabs(["Time Series", "Comparison", "Distribution"])
        
        with tab1:
            try:
                fig_time = st.session_state.visualizer.create_time_series_chart(historical_data)
                if fig_time.data:
                    st.plotly_chart(fig_time, use_container_width=True)
                else:
                    st.info("No time series data available")
            except Exception as e:
                st.error(f"Error creating time series chart: {str(e)}")
        
        with tab2:
            try:
                fig_comparison = st.session_state.visualizer.create_comparison_chart(numeric_kpis, thresholds)
                if fig_comparison.data:
                    st.plotly_chart(fig_comparison, use_container_width=True)
                else:
                    st.info("No comparison data available")
            except Exception as e:
                st.error(f"Error creating comparison chart: {str(e)}")
        
        with tab3:
            try:
                fig_dist = st.session_state.visualizer.create_distribution_chart(historical_data)
                if fig_dist.data:
                    st.plotly_chart(fig_dist, use_container_width=True)
                else:
                    st.info("No distribution data available")
            except Exception as e:
                st.error(f"Error creating distribution chart: {str(e)}")
    else:
        st.info("No historical data available yet. Data will appear here after processing more files.")
    
    # LLM Insights Section
    st.subheader("🤖 AI-Generated Business Insights")
    
    # Get LLM insights
    insights = st.session_state.data_processor.get_llm_insights(data, kpis)
    if insights:
        st.markdown(insights)
    else:
        st.info("AI insights will appear here after data processing with LLM enabled.")
    
    # Suggested Thresholds
    suggested_thresholds = st.session_state.data_processor.get_suggested_thresholds(data, kpis)
    if suggested_thresholds:
        st.subheader("💡 AI-Suggested Thresholds")
        st.info("Based on your historical data, here are AI-recommended thresholds:")
        
        suggestion_cols = st.columns(3)
        for i, (threshold_name, threshold_value) in enumerate(suggested_thresholds.items()):
            with suggestion_cols[i % 3]:
                st.metric(
                    threshold_name.replace('_', ' ').title(),
                    f"{threshold_value:.2f}",
                    help="AI-suggested threshold based on historical data"
                )
    
    # Data table
    st.subheader("Recent Data")
    st.dataframe(data.tail(10), use_container_width=True)
    
    # Export functionality
    st.subheader("Export")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Export Current Data"):
            csv = data.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"kpi_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("Export KPI Report"):
            report = generate_kpi_report(kpis, thresholds)
            st.download_button(
                label="Download Report",
                data=report,
                file_name=f"kpi_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )

def generate_kpi_report(kpis, thresholds):
    """Generate a text report of current KPIs"""
    report = f"KPI Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += "=" * 50 + "\n\n"
    
    for kpi_name, kpi_value in kpis.items():
        threshold = thresholds.get(kpi_name, 0)
        status = "✅ OK" if kpi_value >= threshold else "⚠️ ALERT"
        report += f"{kpi_name.replace('_', ' ').title()}: {kpi_value:.2f} (Threshold: {threshold:.2f}) {status}\n"
    
    return report

if __name__ == "__main__":
    main()
