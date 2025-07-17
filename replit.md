# KPI Dashboard Application

## Overview

This is a real-time business KPI dashboard built with Streamlit that monitors key performance indicators and provides automated alerts when thresholds are breached. The application processes Excel data files, calculates various business metrics, and visualizes them in an interactive dashboard with real-time file monitoring capabilities.

## User Preferences

Preferred communication style: Simple, everyday language.
Technical depth: Comprehensive technical explanations for interview preparation.

## System Architecture

The application follows a modular architecture with clear separation of concerns:

- **Frontend**: Streamlit-based web interface providing real-time dashboard views
- **Data Processing**: Excel file parsing and data cleaning pipeline
- **Database**: SQLite for local data persistence and historical tracking
- **Monitoring**: File system monitoring for automatic data updates
- **Alerting**: Multi-channel alert system (WhatsApp, Slack)
- **Visualization**: Plotly-based interactive charts and graphs

## Key Components

### 1. Main Application (`app.py`)
- Streamlit application entry point
- Session state management for component persistence
- Configuration interface and main dashboard layout
- Coordinates all other components

### 2. Data Processor (`data_processor.py`)
- Excel file loading and parsing (`.xlsx`, `.xls` formats)
- Data cleaning and standardization
- Column validation and type conversion
- Error handling for malformed data

### 3. Database Layer (`database.py`)
- SQLite database for local storage
- Tables: `kpi_data`, `thresholds`, `alerts`
- CRUD operations for KPI data and configuration
- Historical data tracking

### 4. File Monitor (`file_monitor.py`)
- Real-time file system monitoring using watchdog
- Automatic data refresh when Excel files are modified
- Thread-safe file change detection

### 5. KPI Calculator (`kpi_calculator.py`)
- Business metrics calculation engine
- KPIs: revenue, COGS, profit, profit margin, growth rate, efficiency ratios
- Trend analysis and performance metrics
- Configurable calculation methods

### 6. Visualization (`visualization.py`)
- Plotly-based interactive charts
- Time series analysis
- Multi-subplot dashboards
- Customizable color schemes and styling

### 7. Alert Manager (`alert_manager.py`)
- Multi-channel alert system
- WhatsApp Business API integration
- Slack API integration
- Configurable threshold-based alerting

## Data Flow

1. **Data Input**: Users upload Excel files through the Streamlit interface
2. **File Processing**: DataProcessor validates and cleans the data
3. **Storage**: Cleaned data is stored in SQLite database
4. **Monitoring**: FileMonitor watches for file changes and triggers updates
5. **Calculation**: KPICalculator computes metrics from the data
6. **Visualization**: Visualizer creates interactive charts for display
7. **Alerting**: AlertManager sends notifications when thresholds are breached

## External Dependencies

### Core Libraries
- **Streamlit**: Web framework for the dashboard interface
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive visualization library
- **SQLite3**: Local database storage
- **Watchdog**: File system monitoring

### Data Processing
- **NumPy**: Numerical computations
- **OpenPyXL**: Excel file reading (implicit via pandas)

### Alerting Services
- **WhatsApp Business API**: Mobile messaging alerts
- **Slack API**: Team communication alerts
- **Requests**: HTTP client for API calls

### System Integration
- **Threading**: Background file monitoring
- **OS**: File system operations
- **JSON**: Configuration and data serialization

## Deployment Strategy

### Local Development
- SQLite database for local storage
- File-based configuration
- Streamlit development server

### Production Considerations
- The application is designed for local/single-user deployment
- Data persistence through SQLite (may need PostgreSQL for multi-user)
- File monitoring requires local file system access
- API tokens stored in environment variables for security

### Scaling Options
- Database migration to PostgreSQL for multi-user support
- Redis for session management in multi-instance deployments
- Docker containerization for consistent deployment
- Cloud storage integration for file uploads

### Configuration Management
- Environment variables for API tokens
- Database connection strings
- File path configurations
- Alert threshold settings

The architecture prioritizes simplicity and real-time responsiveness while maintaining extensibility for future enhancements like multi-user support, advanced analytics, and cloud deployment.