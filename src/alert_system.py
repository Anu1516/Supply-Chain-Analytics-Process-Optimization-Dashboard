"""
Alert System Module
Automated alerts for supply chain exceptions requiring management escalation
"""

import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import json
import os

class SupplyChainAlertSystem:
    """Generate and send alerts for supply chain exceptions"""

    def __init__(self, config_file='config/alert_config.json'):
        """
        Initialize alert system

        Args:
            config_file: Path to alert configuration file
        """
        self.config = self.load_config(config_file)
        self.alerts = []

    def load_config(self, config_file):
        """Load alert configuration"""
        default_config = {
            'thresholds': {
                'otd_rate_min': 95.0,
                'inventory_turnover_min': 4.0,
                'cycle_time_max_days': 14,
                'delivery_delay_critical_days': 7,
                'stock_out_threshold': 0,
                'excess_stock_days': 90
            },
            'email': {
                'enabled': False,
                'smtp_server': 'smtp.gmail.com',
                'smtp_port': 587,
                'from_email': 'alerts@company.com',
                'to_emails': ['manager@company.com']
            }
        }

        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
            # Merge with defaults
            default_config.update(config)

        return default_config

    def check_otd_alerts(self, kpi_data):
        """
        Check for on-time delivery alerts

        Args:
            kpi_data: KPI data dictionary
        """
        otd_rate = kpi_data['on_time_delivery']['otd_rate_percent']
        threshold = self.config['thresholds']['otd_rate_min']

        if otd_rate < threshold:
            self.alerts.append({
                'type': 'OTD_BELOW_THRESHOLD',
                'severity': 'HIGH',
                'metric': 'On-Time Delivery Rate',
                'current_value': f"{otd_rate}%",
                'threshold': f"{threshold}%",
                'message': f"On-time delivery rate ({otd_rate}%) is below threshold ({threshold}%)",
                'timestamp': datetime.now().isoformat()
            })

    def check_inventory_alerts(self, inventory_df):
        """
        Check for inventory-related alerts

        Args:
            inventory_df: Inventory DataFrame
        """
        # Stock out alerts
        stock_outs = inventory_df[inventory_df['current_stock'] <= self.config['thresholds']['stock_out_threshold']]

        for idx, row in stock_outs.iterrows():
            self.alerts.append({
                'type': 'STOCK_OUT',
                'severity': 'CRITICAL',
                'metric': 'Inventory Stock Level',
                'product_id': row['product_id'],
                'warehouse_id': row['warehouse_id'],
                'current_stock': row['current_stock'],
                'message': f"Stock out alert for Product {row['product_id']} at Warehouse {row['warehouse_id']}",
                'timestamp': datetime.now().isoformat()
            })

        # Excess stock alerts
        excess_stock = inventory_df[inventory_df['stock_age_days'] > self.config['thresholds']['excess_stock_days']]

        for idx, row in excess_stock.iterrows():
            self.alerts.append({
                'type': 'EXCESS_STOCK',
                'severity': 'MEDIUM',
                'metric': 'Inventory Age',
                'product_id': row['product_id'],
                'warehouse_id': row['warehouse_id'],
                'stock_age_days': row['stock_age_days'],
                'stock_value': row['stock_value'],
                'message': f"Excess stock for Product {row['product_id']}: {row['stock_age_days']} days old",
                'timestamp': datetime.now().isoformat()
            })

    def check_delivery_delay_alerts(self, orders_df, logistics_df):
        """
        Check for critical delivery delay alerts

        Args:
            orders_df: Orders DataFrame
            logistics_df: Logistics DataFrame
        """
        df = orders_df.merge(logistics_df, on='order_id', how='left')
        df['expected_delivery_date'] = pd.to_datetime(df['expected_delivery_date'])
        df['actual_arrival'] = pd.to_datetime(df['actual_arrival'])

        # Check for pending deliveries past expected date
        today = pd.Timestamp(datetime.now().date())
        df['delivery_delay_days'] = (today - df['expected_delivery_date']).dt.days

        critical_delays = df[
            (df['actual_arrival'].isna()) &
            (df['delivery_delay_days'] > self.config['thresholds']['delivery_delay_critical_days'])
        ]

        for idx, row in critical_delays.iterrows():
            self.alerts.append({
                'type': 'CRITICAL_DELIVERY_DELAY',
                'severity': 'CRITICAL',
                'metric': 'Delivery Delay',
                'order_id': row['order_id'],
                'supplier_id': row['supplier_id'],
                'delay_days': int(row['delivery_delay_days']),
                'expected_date': row['expected_delivery_date'].strftime('%Y-%m-%d'),
                'message': f"Critical delay for Order {row['order_id']}: {int(row['delivery_delay_days'])} days overdue",
                'timestamp': datetime.now().isoformat()
            })

    def check_supplier_performance_alerts(self, supplier_performance_df):
        """
        Check for supplier performance alerts

        Args:
            supplier_performance_df: Supplier performance DataFrame
        """
        # Alert for suppliers with poor performance
        poor_performers = supplier_performance_df[supplier_performance_df['performance_score'] < 50]

        for supplier_id, row in poor_performers.iterrows():
            self.alerts.append({
                'type': 'POOR_SUPPLIER_PERFORMANCE',
                'severity': 'HIGH',
                'metric': 'Supplier Performance Score',
                'supplier_id': supplier_id,
                'supplier_name': row['supplier_name'],
                'performance_score': row['performance_score'],
                'otd_rate': row['otd_rate'],
                'message': f"Poor performance from {row['supplier_name']} (Score: {row['performance_score']})",
                'timestamp': datetime.now().isoformat()
            })

    def generate_alerts(self, kpi_data, inventory_df, orders_df, logistics_df, supplier_performance_df):
        """
        Generate all alerts

        Args:
            kpi_data: KPI data dictionary
            inventory_df: Inventory DataFrame
            orders_df: Orders DataFrame
            logistics_df: Logistics DataFrame
            supplier_performance_df: Supplier performance DataFrame
        """
        self.alerts = []  # Reset alerts

        # Run all alert checks
        self.check_otd_alerts(kpi_data)
        self.check_inventory_alerts(inventory_df)
        self.check_delivery_delay_alerts(orders_df, logistics_df)
        self.check_supplier_performance_alerts(supplier_performance_df)

        return self.alerts

    def format_alert_email(self, alerts):
        """
        Format alerts for email

        Args:
            alerts: List of alert dictionaries

        Returns:
            HTML formatted email content
        """
        if not alerts:
            return "<html><body><h2>No supply chain alerts at this time.</h2></body></html>"

        # Group by severity
        critical = [a for a in alerts if a['severity'] == 'CRITICAL']
        high = [a for a in alerts if a['severity'] == 'HIGH']
        medium = [a for a in alerts if a['severity'] == 'MEDIUM']

        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                h2 {{ color: #333; }}
                .critical {{ background-color: #ffebee; border-left: 4px solid #f44336; padding: 10px; margin: 10px 0; }}
                .high {{ background-color: #fff3e0; border-left: 4px solid #ff9800; padding: 10px; margin: 10px 0; }}
                .medium {{ background-color: #e8f5e9; border-left: 4px solid #4caf50; padding: 10px; margin: 10px 0; }}
                .alert-type {{ font-weight: bold; color: #666; }}
                .alert-message {{ margin: 5px 0; }}
            </style>
        </head>
        <body>
            <h1>Supply Chain Alert Report</h1>
            <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>Total Alerts: {len(alerts)}</strong></p>
        """

        if critical:
            html += f"<h2>Critical Alerts ({len(critical)})</h2>"
            for alert in critical:
                html += f"""
                <div class="critical">
                    <div class="alert-type">{alert['type']}</div>
                    <div class="alert-message">{alert['message']}</div>
                </div>
                """

        if high:
            html += f"<h2>High Priority Alerts ({len(high)})</h2>"
            for alert in high:
                html += f"""
                <div class="high">
                    <div class="alert-type">{alert['type']}</div>
                    <div class="alert-message">{alert['message']}</div>
                </div>
                """

        if medium:
            html += f"<h2>Medium Priority Alerts ({len(medium)})</h2>"
            for alert in medium:
                html += f"""
                <div class="medium">
                    <div class="alert-type">{alert['type']}</div>
                    <div class="alert-message">{alert['message']}</div>
                </div>
                """

        html += "</body></html>"
        return html

    def send_email_alerts(self, alerts):
        """
        Send email alerts

        Args:
            alerts: List of alert dictionaries
        """
        if not self.config['email']['enabled'] or not alerts:
            print("Email alerts disabled or no alerts to send")
            return

        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"Supply Chain Alerts - {datetime.now().strftime('%Y-%m-%d')}"
        msg['From'] = self.config['email']['from_email']
        msg['To'] = ', '.join(self.config['email']['to_emails'])

        html_content = self.format_alert_email(alerts)
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)

        try:
            with smtplib.SMTP(self.config['email']['smtp_server'], self.config['email']['smtp_port']) as server:
                server.starttls()
                # In production, use secure credentials management
                # server.login(username, password)
                server.send_message(msg)
            print(f"Alert email sent to {msg['To']}")
        except Exception as e:
            print(f"Failed to send email: {e}")

    def save_alerts_to_file(self, alerts, output_file='data/alerts_log.json'):
        """
        Save alerts to JSON file

        Args:
            alerts: List of alert dictionaries
            output_file: Path to output file
        """
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # Load existing alerts
        existing_alerts = []
        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                existing_alerts = json.load(f)

        # Append new alerts
        existing_alerts.extend(alerts)

        # Save
        with open(output_file, 'w') as f:
            json.dump(existing_alerts, f, indent=2)

        print(f"Alerts saved to {output_file}")

    def print_alerts(self, alerts):
        """Print alerts to console"""
        if not alerts:
            print("\nNo alerts generated.")
            return

        print("\n" + "="*60)
        print("SUPPLY CHAIN ALERTS")
        print("="*60)

        critical = [a for a in alerts if a['severity'] == 'CRITICAL']
        high = [a for a in alerts if a['severity'] == 'HIGH']
        medium = [a for a in alerts if a['severity'] == 'MEDIUM']

        if critical:
            print(f"\n[CRITICAL] - {len(critical)} alerts")
            for alert in critical:
                print(f"  - {alert['message']}")

        if high:
            print(f"\n[HIGH] - {len(high)} alerts")
            for alert in high:
                print(f"  - {alert['message']}")

        if medium:
            print(f"\n[MEDIUM] - {len(medium)} alerts")
            for alert in medium:
                print(f"  - {alert['message']}")

        print("\n" + "="*60)

if __name__ == "__main__":
    print("Supply Chain Alert System")
    print("Run this module after calculating KPIs")
