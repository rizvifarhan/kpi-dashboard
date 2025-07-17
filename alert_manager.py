import requests
import os
import json
from datetime import datetime
import streamlit as st

class AlertManager:
    def __init__(self):
        self.whatsapp_token = None
        self.whatsapp_phone = None
        self.slack_token = None
        self.slack_channel = None
    
    def configure_whatsapp(self, token, phone):
        """Configure WhatsApp alert settings"""
        self.whatsapp_token = token
        self.whatsapp_phone = phone
    
    def configure_slack(self, token, channel):
        """Configure Slack alert settings"""
        self.slack_token = token
        self.slack_channel = channel
    
    def send_alert(self, message):
        """Send alert via configured channels"""
        success = False
        
        # Send WhatsApp alert
        if self.whatsapp_token and self.whatsapp_phone:
            success = self.send_whatsapp_message(message) or success
        
        # Send Slack alert
        if self.slack_token and self.slack_channel:
            success = self.send_slack_message(message) or success
        
        return success
    
    def send_whatsapp_message(self, message):
        """Send WhatsApp message using WhatsApp Business API"""
        try:
            url = f"https://graph.facebook.com/v17.0/your_phone_number_id/messages"
            
            headers = {
                "Authorization": f"Bearer {self.whatsapp_token}",
                "Content-Type": "application/json"
            }
            
            data = {
                "messaging_product": "whatsapp",
                "to": self.whatsapp_phone,
                "type": "text",
                "text": {
                    "body": message
                }
            }
            
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 200:
                st.success("WhatsApp alert sent successfully!")
                return True
            else:
                st.error(f"Failed to send WhatsApp alert: {response.text}")
                return False
                
        except Exception as e:
            st.error(f"Error sending WhatsApp message: {str(e)}")
            return False
    
    def send_slack_message(self, message):
        """Send Slack message using Slack API"""
        try:
            url = "https://slack.com/api/chat.postMessage"
            
            headers = {
                "Authorization": f"Bearer {self.slack_token}",
                "Content-Type": "application/json"
            }
            
            data = {
                "channel": self.slack_channel,
                "text": message,
                "username": "KPI Dashboard Bot",
                "icon_emoji": ":chart_with_upwards_trend:"
            }
            
            response = requests.post(url, headers=headers, json=data)
            result = response.json()
            
            if result.get("ok"):
                st.success("Slack alert sent successfully!")
                return True
            else:
                st.error(f"Failed to send Slack alert: {result.get('error', 'Unknown error')}")
                return False
                
        except Exception as e:
            st.error(f"Error sending Slack message: {str(e)}")
            return False
    
    def format_alert_message(self, kpi_name, current_value, threshold, trend_direction="stable"):
        """Format alert message with relevant information"""
        trend_emoji = {
            "up": "📈",
            "down": "📉",
            "stable": "➡️"
        }
        
        message = f"""
🚨 KPI ALERT 🚨

Metric: {kpi_name.replace('_', ' ').title()}
Current Value: {current_value:.2f}
Threshold: {threshold:.2f}
Trend: {trend_emoji.get(trend_direction, '➡️')} {trend_direction.title()}

Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Please review and take necessary action.
        """.strip()
        
        return message
    
    def send_threshold_alert(self, kpi_name, current_value, threshold, trend_direction="stable"):
        """Send formatted threshold alert"""
        message = self.format_alert_message(kpi_name, current_value, threshold, trend_direction)
        return self.send_alert(message)
    
    def send_system_alert(self, alert_type, details):
        """Send system-related alerts"""
        message = f"""
🔧 SYSTEM ALERT 🔧

Type: {alert_type}
Details: {details}
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """.strip()
        
        return self.send_alert(message)
    
    def test_configuration(self):
        """Test alert configuration"""
        test_message = f"🧪 Test Alert - KPI Dashboard\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        return self.send_alert(test_message)
