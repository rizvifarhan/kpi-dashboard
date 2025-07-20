# 📊 KPI Dashboard - Real-Time Business Intelligence

A powerful real-time business intelligence platform that transforms raw Excel data into actionable insights through advanced analytics, automated alerting, and interactive visualizations.

## ✨ Features

- **🤖 AI-Powered Data Extraction**: Uses Qwen3B AI to intelligently understand Excel data regardless of column names
- **📈 Real-Time KPI Monitoring**: Automatic calculation of revenue, profit margins, growth rates, and trends
- **🔔 Smart Alerting**: WhatsApp and Slack notifications when metrics fall below thresholds
- **📊 Interactive Visualizations**: Time series, comparison charts, and distribution analysis
- **🔄 Live File Monitoring**: Automatically updates when Excel files change
- **💡 Business Insights**: AI-generated recommendations and threshold suggestions

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/kpi-dashboard.git
cd kpi-dashboard
```

### 2. Install Dependencies
```bash
pip install streamlit pandas plotly numpy openpyxl watchdog requests openai
```

### 3. Set Environment Variables
```bash
export OPENROUTER_API_KEY="your_openrouter_api_key"
export WHATSAPP_TOKEN="your_whatsapp_token"  # Optional
export SLACK_TOKEN="your_slack_bot_token"    # Optional
```

### 4. Run the Application
```bash
streamlit run app.py
```

### 5. Upload Your Excel File
- Open the dashboard in your browser
- Upload your business data Excel file
- Watch as AI analyzes and visualizes your KPIs

## 📁 Project Structure

```
kpi-dashboard/
├── app.py                 # Main Streamlit application
├── data_processor.py      # Excel data processing with AI
├── llm_data_extractor.py  # AI-powered data analysis
├── kpi_calculator.py      # Business metrics calculation
├── database.py            # SQLite data persistence
├── alert_manager.py       # Multi-channel alerting
├── visualization.py       # Interactive charts
├── file_monitor.py        # Real-time file monitoring
├── DEPLOYMENT_GUIDE.md    # Deployment instructions
├── TECHNICAL_OVERVIEW.md  # Technical documentation
└── requirements.txt       # Python dependencies
```

## 🔧 Configuration

### Required Environment Variables
- `OPENROUTER_API_KEY`: For AI-powered data analysis

### Optional Environment Variables
- `WHATSAPP_TOKEN`: WhatsApp Business API token for mobile alerts
- `WHATSAPP_PHONE`: Your WhatsApp phone number
- `SLACK_TOKEN`: Slack bot token for team notifications
- `SLACK_CHANNEL`: Slack channel for alerts (default: #alerts)

## 📊 Supported Data Formats

Your Excel file should contain business data with columns like:
- Date/Time information
- Revenue/Sales/Income data
- Cost of Goods Sold (COGS)/Expenses
- Any other business metrics

The AI automatically identifies and maps these columns regardless of naming conventions.

## 🤖 AI Features

- **Smart Column Mapping**: Automatically identifies revenue, COGS, date columns
- **Business Insights**: Generates actionable recommendations based on your data
- **Threshold Suggestions**: AI recommends optimal alert thresholds
- **Data Quality Analysis**: Provides confidence scores and processing suggestions

## 🚀 Deployment Options

### Free Hosting
- **Streamlit Community Cloud**: Deploy directly from GitHub for free
- **Replit**: Host on Replit platform

### Paid Hosting
- **Railway**: $5/month, modern platform with automatic scaling
- **Render**: $19/month, reliable with background workers
- **AWS/GCP/Azure**: Enterprise deployment options

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.

## 📈 Key Performance Indicators

The dashboard automatically calculates:
- **Revenue Metrics**: Total revenue, growth rates, trends
- **Profitability**: Profit margins, COGS analysis
- **Operational KPIs**: Efficiency ratios, performance trends
- **Forecasting**: Moving averages and trend predictions

## 🔔 Alert System

- **Real-time Monitoring**: Continuous threshold checking
- **Multi-channel Alerts**: WhatsApp, Slack, and dashboard notifications
- **Smart Thresholds**: AI-suggested optimal alert levels
- **Alert History**: Complete log of all notifications

## 🛠️ Technology Stack

- **Frontend**: Streamlit for interactive web interface
- **AI/ML**: Qwen3B via OpenRouter for intelligent data processing
- **Data Processing**: Pandas, NumPy for data manipulation
- **Visualization**: Plotly for interactive charts
- **Database**: SQLite for local data persistence
- **Monitoring**: Watchdog for file system monitoring
- **APIs**: WhatsApp Business API, Slack API

## 📚 Documentation

- [Technical Overview](TECHNICAL_OVERVIEW.md): Detailed architecture and code flow
- [Interview Guide](INTERVIEW_PREPARATION.md): Technical interview preparation
- [Deployment Guide](DEPLOYMENT_GUIDE.md): Hosting and deployment options
- [Code Flow Diagram](CODE_FLOW_DIAGRAM.md): System architecture visualization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🎯 Use Cases

- **Small Businesses**: Monitor daily/weekly performance metrics
- **Startups**: Track growth KPIs and investor metrics
- **Sales Teams**: Real-time revenue and pipeline monitoring
- **Finance Teams**: Automated financial reporting and alerts
- **Management**: Executive dashboard for key business insights

## 🔮 Future Enhancements

- Machine learning predictions and forecasting
- Advanced anomaly detection
- Multi-user authentication and role management
- Custom dashboard builder
- API endpoints for external integrations
- Mobile app companion

---

Built with ❤️ using modern Python technologies and AI for intelligent business monitoring.