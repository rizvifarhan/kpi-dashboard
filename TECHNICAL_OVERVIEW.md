# KPI Dashboard - Technical Overview & Interview Guide

## 🚀 Project Overview
A real-time business KPI dashboard that monitors Excel data files, calculates key performance indicators, and sends automated alerts when metrics fall below predefined thresholds. Built with Python and Streamlit for rapid prototyping and deployment.

## 🛠️ Tech Stack

### Frontend & Framework
- **Streamlit** (Main Framework)
  - Web-based dashboard interface
  - Real-time data visualization
  - Interactive widgets and forms
  - Session state management

### Backend & Data Processing
- **Python 3.11** (Core Language)
- **Pandas** (Data Manipulation)
  - Excel file processing
  - Data cleaning and transformation
  - Time series analysis
- **NumPy** (Numerical Computing)
  - Statistical calculations
  - Mathematical operations for KPIs

### Database & Storage
- **SQLite3** (Local Database)
  - KPI data storage
  - Threshold configuration
  - Historical data tracking
  - Alert logging

### Data Visualization
- **Plotly** (Interactive Charts)
  - Time series charts
  - Comparison charts
  - Distribution histograms
  - Gauge charts
  - Heatmaps

### File System & Monitoring
- **Watchdog** (File Monitoring)
  - Real-time file change detection
  - Automatic data refresh
  - Thread-safe monitoring
- **OpenPyXL** (Excel Processing)
  - .xlsx file support
  - Data extraction

### External Integrations
- **WhatsApp Business API** (Alerts)
  - REST API integration
  - Automated messaging
- **Slack API** (Team Notifications)
  - Bot integration
  - Channel messaging
- **Requests** (HTTP Client)
  - API communication
  - Error handling

### Development & Deployment
- **Threading** (Background Tasks)
- **JSON** (Data Serialization)
- **OS/Datetime** (System Integration)

## 🏗️ Architecture & Design Patterns

### 1. Modular Architecture
```
app.py              # Main application entry point
├── data_processor.py    # Data loading and cleaning
├── kpi_calculator.py    # Business logic for metrics
├── database.py          # Data persistence layer
├── alert_manager.py     # Notification system
├── visualization.py     # Chart generation
└── file_monitor.py      # File system monitoring
```

### 2. Design Patterns Used
- **Singleton Pattern**: Session state management
- **Observer Pattern**: File monitoring system
- **Strategy Pattern**: Multiple alert channels
- **Factory Pattern**: Chart creation
- **MVC Pattern**: Model-View-Controller separation

### 3. Object-Oriented Design
- **Encapsulation**: Each module handles specific responsibilities
- **Abstraction**: Clean interfaces between components
- **Composition**: Components work together through dependency injection

## 🔄 Code Flow & Execution

### 1. Application Startup
```python
# app.py - main()
1. Initialize Streamlit configuration
2. Create session state objects:
   - DataProcessor()
   - KPICalculator()
   - Database()
   - AlertManager()
   - Visualizer()
3. Render UI components
```

### 2. Data Processing Pipeline
```python
# When user uploads Excel file:
1. app.py → process_uploaded_file()
2. DataProcessor.load_excel() → Clean & validate data
3. KPICalculator.calculate_kpis() → Compute metrics
4. Database.store_data() → Persist to SQLite
5. check_thresholds() → Trigger alerts if needed
6. display_dashboard() → Render visualizations
```

### 3. Real-time Monitoring
```python
# File monitoring workflow:
1. FileMonitor.start_monitoring() → Watch for file changes
2. ExcelFileHandler.on_modified() → Detect changes
3. Callback function → Trigger data refresh
4. Auto-refresh mechanism → Update dashboard
```

### 4. Alert System
```python
# Alert workflow:
1. check_thresholds() → Compare KPIs vs thresholds
2. AlertManager.send_alert() → Route to channels
3. send_whatsapp_message() / send_slack_message()
4. Database.log_alert() → Record alert history
```

## 🎯 Key Technical Concepts

### 1. Data Validation & Cleaning
```python
# data_processor.py
- Column name standardization
- Data type conversion
- Missing value handling
- Date parsing and validation
- Anomaly detection using z-scores
```

### 2. KPI Calculation Engine
```python
# kpi_calculator.py
- Revenue, COGS, Profit calculations
- Profit margin percentages
- Growth rate analysis
- Moving averages (7, 14, 30 day)
- Trend analysis using linear regression
- Seasonal performance metrics
```

### 3. Database Schema
```sql
-- SQLite Tables
kpi_data: id, timestamp, date, revenue, cogs, profit, profit_margin, growth_rate, raw_data
thresholds: id, kpi_name, threshold_value, created_at, updated_at
alerts: id, kpi_name, current_value, threshold_value, alert_type, message, sent_at, status
```

### 4. Session State Management
```python
# Streamlit session state
- Persistent component instances
- Data caching between requests
- File upload state tracking
- Configuration management
```

## 🚨 Error Handling & Resilience

### 1. Data Validation
- Type checking for all numeric operations
- Graceful handling of missing columns
- Excel format validation
- Date parsing error recovery

### 2. Visualization Robustness
- JSON serialization error handling
- Empty data graceful fallbacks
- Chart rendering error recovery
- Data type conversion safety

### 3. Database Operations
- Transaction rollback on errors
- Connection management
- Schema validation
- Data integrity checks

## 🔍 Performance Considerations

### 1. Data Processing
- Efficient pandas operations
- Memory-conscious data loading
- Incremental data updates
- Batch processing for large files

### 2. Visualization
- Lazy loading of charts
- Data sampling for large datasets
- Efficient plotly figure generation
- Client-side rendering optimization

### 3. Caching Strategy
- Session state caching
- Database query optimization
- File modification time checking
- Conditional data refresh

## 🧪 Testing Strategy

### 1. Unit Testing Components
```python
# test_dashboard.py demonstrates:
- Data loading validation
- KPI calculation accuracy
- Database operations
- Alert functionality
- Visualization generation
```

### 2. Integration Testing
- End-to-end data flow
- Component interaction
- API integration testing
- Error scenario handling

## 🚀 Deployment & Scalability

### 1. Current Setup
- Local SQLite database
- File-based configuration
- Single-user design
- Streamlit development server

### 2. Production Considerations
- PostgreSQL for multi-user support
- Redis for session management
- Docker containerization
- Cloud storage integration
- Load balancing for multiple instances

## 📊 Key Features Implemented

### 1. Core Functionality
- Excel file upload and processing
- Real-time KPI calculations
- Interactive dashboard
- Threshold-based alerting
- Historical data tracking

### 2. Advanced Features
- Multiple visualization types
- Moving averages calculation
- Trend analysis
- Seasonal performance tracking
- Data export capabilities

### 3. User Experience
- Responsive design
- Real-time updates
- Intuitive threshold configuration
- Error-friendly interface
- Progress indicators

## 💡 Interview Talking Points

### 1. Technical Challenges Solved
- **Data Type Handling**: Robust type conversion and validation
- **JSON Serialization**: Fixed Plotly chart serialization issues
- **Real-time Updates**: Implemented file monitoring and auto-refresh
- **Error Recovery**: Comprehensive error handling throughout

### 2. Design Decisions
- **Modular Architecture**: Easy to maintain and extend
- **SQLite Choice**: Rapid prototyping with potential for upgrade
- **Streamlit Framework**: Fast development with rich UI components
- **Pandas Integration**: Efficient data manipulation

### 3. Future Enhancements
- Machine learning predictions
- Advanced analytics
- Multi-tenant support
- Mobile responsiveness
- API endpoints for external integration

## 🎬 Demo Script
1. **Data Upload**: Show Excel file processing
2. **KPI Display**: Explain calculated metrics
3. **Threshold Config**: Demonstrate alert setup
4. **Visualizations**: Walk through different chart types
5. **Alert System**: Show notification configuration
6. **Export Features**: Demonstrate data export

This comprehensive technical overview should prepare you for discussing the project architecture, implementation details, and design decisions during your interview.