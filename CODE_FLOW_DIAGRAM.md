# KPI Dashboard - Code Flow & Architecture Diagram

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        STREAMLIT FRONTEND                       │
├─────────────────────────────────────────────────────────────────┤
│  📊 Dashboard UI  │  📁 File Upload  │  ⚙️ Config Panel        │
│  • KPI Metrics   │  • Excel Files   │  • Thresholds            │
│  • Charts/Graphs │  • Drag & Drop   │  • Alert Settings        │
│  • Data Tables   │  • Validation    │  • API Tokens            │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      SESSION STATE LAYER                        │
├─────────────────────────────────────────────────────────────────┤
│  • DataProcessor    • KPICalculator    • Database               │
│  • AlertManager     • Visualizer       • FileMonitor           │
│  • Current Data     • Last Update      • File Path             │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                       BUSINESS LOGIC                            │
├─────────────────────────────────────────────────────────────────┤
│  📈 KPI Calculator  │  📊 Visualizer    │  🔔 Alert Manager     │
│  • Revenue/Profit   │  • Time Series    │  • WhatsApp API       │
│  • Margins/Growth   │  • Comparisons    │  • Slack API          │
│  • Trends/Forecasts │  • Distributions  │  • Threshold Checks   │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                        DATA LAYER                               │
├─────────────────────────────────────────────────────────────────┤
│  📁 Data Processor  │  🗄️ SQLite DB     │  👁️ File Monitor     │
│  • Excel Parsing    │  • KPI Storage    │  • Change Detection   │
│  • Data Cleaning    │  • Thresholds     │  • Auto Refresh      │
│  • Validation       │  • Alert Logs     │  • Threading          │
└─────────────────────────────────────────────────────────────────┘
```

## 🔄 Data Flow Process

### 1. User Upload Flow
```
User Upload Excel File
        │
        ▼
┌─────────────────────┐
│   app.py:main()     │ ← Streamlit Entry Point
│   file_uploader()   │
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│ process_uploaded_   │ ← File Processing
│ file(file_path)     │
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│ DataProcessor.      │ ← Data Cleaning
│ load_excel()        │
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│ KPICalculator.      │ ← Business Logic
│ calculate_kpis()    │
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│ Database.           │ ← Data Persistence
│ store_data()        │
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│ check_thresholds()  │ ← Alert Logic
│ AlertManager.       │
│ send_alert()        │
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│ display_dashboard() │ ← UI Update
│ Visualizer.create_  │
│ charts()            │
└─────────────────────┘
```

### 2. Real-time Monitoring Flow
```
File System Change
        │
        ▼
┌─────────────────────┐
│ FileMonitor.        │ ← Watchdog Observer
│ start_monitoring()  │
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│ ExcelFileHandler.   │ ← Event Handler
│ on_modified()       │
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│ Callback Function   │ ← Trigger Update
│ process_file()      │
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│ st.rerun()          │ ← UI Refresh
└─────────────────────┘
```

### 3. Alert System Flow
```
KPI Calculation Complete
        │
        ▼
┌─────────────────────┐
│ check_thresholds()  │ ← Threshold Check
│ Database.get_       │
│ thresholds()        │
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│ AlertManager.       │ ← Alert Routing
│ send_alert()        │
└─────────────────────┘
        │
        ├─────────────────┬─────────────────┐
        ▼                 ▼                 ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ WhatsApp    │  │ Slack API   │  │ Database    │
│ Business    │  │ Integration │  │ Alert Log   │
│ API         │  │             │  │             │
└─────────────┘  └─────────────┘  └─────────────┘
```

## 🎯 Key Technical Implementation Details

### 1. Session State Management
```python
# app.py - Session State Initialization
if 'data_processor' not in st.session_state:
    st.session_state.data_processor = DataProcessor()
if 'kpi_calculator' not in st.session_state:
    st.session_state.kpi_calculator = KPICalculator()
# ... other components
```

### 2. Data Processing Pipeline
```python
# data_processor.py - Core Processing
def load_excel(file_path):
    df = pd.read_excel(file_path)
    df = self.clean_data(df)
    if self.validate_data(df):
        return df
    return None

def clean_data(df):
    # Standardize column names
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    # Convert data types
    # Handle missing values
    # Sort by date
    return df
```

### 3. KPI Calculation Engine
```python
# kpi_calculator.py - Business Logic
def calculate_kpis(data):
    kpis = {
        'revenue': self.calculate_revenue(data),
        'profit': self.calculate_profit(data),
        'profit_margin': self.calculate_profit_margin(data),
        'growth_rate': self.calculate_growth_rate(data),
        # ... more KPIs
    }
    # Add trend analysis
    kpis.update(self.calculate_trends(data))
    return kpis
```

### 4. Database Operations
```python
# database.py - Data Persistence
def store_data(data, kpis):
    conn = sqlite3.connect(self.db_path)
    cursor = conn.cursor()
    
    for _, row in data.iterrows():
        cursor.execute('''
            INSERT INTO kpi_data 
            (date, revenue, cogs, profit, profit_margin, growth_rate, raw_data)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (values...))
    
    conn.commit()
    conn.close()
```

### 5. Visualization Generation
```python
# visualization.py - Chart Creation
def create_time_series_chart(data):
    fig = make_subplots(rows=2, cols=2)
    
    # Add traces for each KPI
    fig.add_trace(go.Scatter(x=x_axis, y=revenue_data), row=1, col=1)
    fig.add_trace(go.Scatter(x=x_axis, y=profit_data), row=1, col=2)
    
    fig.update_layout(title="KPI Trends Over Time")
    return fig
```

## 🔧 Error Handling Strategy

### 1. Data Validation Layers
```python
# Multiple validation checkpoints
try:
    data = data_processor.load_excel(file_path)
    if data is None:
        st.error("Invalid file format")
        return
    
    kpis = kpi_calculator.calculate_kpis(data)
    database.store_data(data, kpis)
    
except Exception as e:
    st.error(f"Processing error: {str(e)}")
    # Log error for debugging
```

### 2. Visualization Error Handling
```python
# Robust chart generation
try:
    fig = visualizer.create_time_series_chart(data)
    if fig.data:
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available for visualization")
except Exception as e:
    st.error(f"Chart generation error: {str(e)}")
```

## 🚀 Performance Optimizations

### 1. Data Processing
- Efficient pandas operations
- Memory-conscious loading
- Batch processing for large files
- Incremental updates

### 2. Caching Strategy
- Session state persistence
- Database query optimization
- Conditional data refresh
- File modification checking

### 3. UI Responsiveness
- Lazy loading of charts
- Progress indicators
- Async processing where possible
- Error boundary implementation

## 📱 Component Interaction Map

```
app.py (Main Controller)
├── DataProcessor (data_processor.py)
│   ├── Excel file parsing
│   ├── Data cleaning
│   └── Validation
├── KPICalculator (kpi_calculator.py)
│   ├── Revenue calculations
│   ├── Profit analysis
│   ├── Growth trends
│   └── Moving averages
├── Database (database.py)
│   ├── SQLite operations
│   ├── Data storage
│   ├── Threshold management
│   └── Alert logging
├── AlertManager (alert_manager.py)
│   ├── WhatsApp integration
│   ├── Slack integration
│   └── Threshold monitoring
├── Visualizer (visualization.py)
│   ├── Time series charts
│   ├── Comparison charts
│   ├── Distribution plots
│   └── Dashboard metrics
└── FileMonitor (file_monitor.py)
    ├── File system watching
    ├── Change detection
    └── Auto-refresh triggers
```

This comprehensive technical overview should give you a solid foundation for discussing the project architecture, implementation details, and design decisions during your interview. The modular design, error handling, and real-time capabilities demonstrate strong software engineering practices.