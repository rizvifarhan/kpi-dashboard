import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import json

class Database:
    def __init__(self, db_path="kpi_dashboard.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create data table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS kpi_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                date DATE,
                revenue REAL,
                cogs REAL,
                profit REAL,
                profit_margin REAL,
                growth_rate REAL,
                raw_data TEXT
            )
        ''')
        
        # Create thresholds table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS thresholds (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kpi_name TEXT UNIQUE,
                threshold_value REAL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create alerts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kpi_name TEXT,
                current_value REAL,
                threshold_value REAL,
                alert_type TEXT,
                message TEXT,
                sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'sent'
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def store_data(self, data, kpis):
        """Store processed data and KPIs"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Store each row of data
            for _, row in data.iterrows():
                # Convert date to string if it's a timestamp
                date_value = row.get('date', datetime.now().date())
                if hasattr(date_value, 'strftime'):
                    date_value = date_value.strftime('%Y-%m-%d')
                elif hasattr(date_value, 'date'):
                    date_value = date_value.date().strftime('%Y-%m-%d')
                
                cursor.execute('''
                    INSERT INTO kpi_data 
                    (date, revenue, cogs, profit, profit_margin, growth_rate, raw_data)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    date_value,
                    float(row.get('revenue', 0)),
                    float(row.get('cogs', 0)),
                    float(kpis.get('profit', 0)),
                    float(kpis.get('profit_margin', 0)),
                    float(kpis.get('growth_rate', 0)),
                    json.dumps(row.to_dict(), default=str)
                ))
            
            conn.commit()
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def get_historical_data(self, days=30):
        """Get historical data for specified number of days"""
        conn = sqlite3.connect(self.db_path)
        
        query = '''
            SELECT * FROM kpi_data 
            WHERE timestamp >= datetime('now', '-{} days')
            ORDER BY timestamp DESC
        '''.format(days)
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        return df
    
    def get_thresholds(self):
        """Get all configured thresholds"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT kpi_name, threshold_value FROM thresholds')
        results = cursor.fetchall()
        
        conn.close()
        
        return {row[0]: row[1] for row in results}
    
    def update_threshold(self, kpi_name, threshold_value):
        """Update or insert threshold for a KPI"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO thresholds 
            (kpi_name, threshold_value, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        ''', (kpi_name, threshold_value))
        
        conn.commit()
        conn.close()
    
    def log_alert(self, kpi_name, current_value, threshold_value, alert_type, message):
        """Log sent alert"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO alerts 
            (kpi_name, current_value, threshold_value, alert_type, message)
            VALUES (?, ?, ?, ?, ?)
        ''', (kpi_name, current_value, threshold_value, alert_type, message))
        
        conn.commit()
        conn.close()
    
    def get_recent_alerts(self, hours=24):
        """Get recent alerts to avoid spam"""
        conn = sqlite3.connect(self.db_path)
        
        query = '''
            SELECT * FROM alerts 
            WHERE sent_at >= datetime('now', '-{} hours')
            ORDER BY sent_at DESC
        '''.format(hours)
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        return df
    
    def get_kpi_summary(self, days=7):
        """Get KPI summary for the last N days"""
        conn = sqlite3.connect(self.db_path)
        
        query = '''
            SELECT 
                AVG(revenue) as avg_revenue,
                AVG(profit) as avg_profit,
                AVG(profit_margin) as avg_profit_margin,
                AVG(growth_rate) as avg_growth_rate,
                COUNT(*) as data_points
            FROM kpi_data 
            WHERE timestamp >= datetime('now', '-{} days')
        '''.format(days)
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        return df.iloc[0].to_dict() if not df.empty else {}
    
    def cleanup_old_data(self, days=90):
        """Clean up old data to prevent database bloat"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Delete old data records
        cursor.execute('''
            DELETE FROM kpi_data 
            WHERE timestamp < datetime('now', '-{} days')
        '''.format(days))
        
        # Delete old alerts
        cursor.execute('''
            DELETE FROM alerts 
            WHERE sent_at < datetime('now', '-{} days')
        '''.format(days))
        
        conn.commit()
        conn.close()
    
    def export_data(self, table_name, format='csv'):
        """Export data from specified table"""
        conn = sqlite3.connect(self.db_path)
        
        df = pd.read_sql_query(f'SELECT * FROM {table_name}', conn)
        conn.close()
        
        if format == 'csv':
            return df.to_csv(index=False)
        elif format == 'json':
            return df.to_json(orient='records', indent=2)
        
        return df
