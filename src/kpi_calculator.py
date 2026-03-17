"""
KPI Calculator Module
Calculates key performance indicators for supply chain analytics
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class SupplyChainKPICalculator:
    """Calculate supply chain KPIs from extracted data"""

    def __init__(self, orders_df, suppliers_df, inventory_df, logistics_df):
        """
        Initialize KPI calculator with data

        Args:
            orders_df: DataFrame with orders data
            suppliers_df: DataFrame with supplier data
            inventory_df: DataFrame with inventory data
            logistics_df: DataFrame with logistics data
        """
        self.orders = orders_df
        self.suppliers = suppliers_df
        self.inventory = inventory_df
        self.logistics = logistics_df

    def calculate_on_time_delivery_rate(self):
        """
        Calculate on-time delivery rate

        Returns:
            Dictionary with OTD metrics
        """
        # Merge orders with logistics
        df = self.orders.merge(self.logistics, on='order_id', how='left')

        # Convert date columns
        df['expected_delivery_date'] = pd.to_datetime(df['expected_delivery_date'])
        df['actual_arrival'] = pd.to_datetime(df['actual_arrival'])

        # Calculate on-time deliveries
        df['is_on_time'] = df['actual_arrival'] <= df['expected_delivery_date']
        df['delivery_delay_days'] = (df['actual_arrival'] - df['expected_delivery_date']).dt.days

        # Calculate metrics
        total_delivered = df[df['actual_arrival'].notna()].shape[0]
        on_time_count = df[df['is_on_time'] == True].shape[0]
        otd_rate = (on_time_count / total_delivered * 100) if total_delivered > 0 else 0

        avg_delay = df[df['delivery_delay_days'] > 0]['delivery_delay_days'].mean()

        return {
            'otd_rate_percent': round(otd_rate, 2),
            'total_deliveries': total_delivered,
            'on_time_deliveries': on_time_count,
            'late_deliveries': total_delivered - on_time_count,
            'average_delay_days': round(avg_delay, 1) if not pd.isna(avg_delay) else 0
        }

    def calculate_inventory_turnover(self):
        """
        Calculate inventory turnover ratio

        Returns:
            Dictionary with inventory turnover metrics
        """
        # Calculate total inventory value
        total_inventory_value = self.inventory['stock_value'].sum()

        # Calculate COGS from orders (approximation)
        total_cogs = self.orders['total_amount'].sum()

        # Calculate turnover ratio
        turnover_ratio = total_cogs / total_inventory_value if total_inventory_value > 0 else 0

        # Days inventory outstanding
        dio = 365 / turnover_ratio if turnover_ratio > 0 else 0

        # Identify slow-moving items
        slow_moving = self.inventory[self.inventory['stock_age_days'] > 90].copy()

        return {
            'inventory_turnover_ratio': round(turnover_ratio, 2),
            'days_inventory_outstanding': round(dio, 1),
            'total_inventory_value': round(total_inventory_value, 2),
            'slow_moving_items_count': len(slow_moving),
            'slow_moving_value': round(slow_moving['stock_value'].sum(), 2)
        }

    def calculate_supplier_performance(self):
        """
        Calculate supplier performance scores

        Returns:
            DataFrame with supplier performance metrics
        """
        # Merge orders with suppliers
        df = self.orders.merge(self.suppliers, on='supplier_id', how='left')

        # Calculate metrics per supplier
        supplier_metrics = df.groupby('supplier_id').agg({
            'order_id': 'count',
            'total_amount': 'sum',
            'supplier_name': 'first',
            'rating': 'first'
        }).rename(columns={'order_id': 'total_orders', 'total_amount': 'total_spend'})

        # Calculate on-time delivery per supplier
        df_with_logistics = df.merge(self.logistics, on='order_id', how='left')
        df_with_logistics['expected_delivery_date'] = pd.to_datetime(df_with_logistics['expected_delivery_date'])
        df_with_logistics['actual_arrival'] = pd.to_datetime(df_with_logistics['actual_arrival'])
        df_with_logistics['is_on_time'] = df_with_logistics['actual_arrival'] <= df_with_logistics['expected_delivery_date']

        otd_by_supplier = df_with_logistics.groupby('supplier_id').agg({
            'is_on_time': lambda x: (x.sum() / len(x) * 100) if len(x) > 0 else 0
        }).rename(columns={'is_on_time': 'otd_rate'})

        supplier_metrics = supplier_metrics.join(otd_by_supplier)

        # Calculate composite performance score
        # Score = (OTD Rate * 0.5) + (Rating * 10)
        supplier_metrics['performance_score'] = (
            supplier_metrics['otd_rate'] * 0.5 +
            supplier_metrics['rating'] * 10
        )

        supplier_metrics = supplier_metrics.round(2)
        supplier_metrics = supplier_metrics.sort_values('performance_score', ascending=False)

        return supplier_metrics

    def calculate_service_level_failures(self):
        """
        Identify and categorize service level failures

        Returns:
            Dictionary with failure metrics
        """
        # Merge data
        df = self.orders.merge(self.logistics, on='order_id', how='left')
        df['expected_delivery_date'] = pd.to_datetime(df['expected_delivery_date'])
        df['actual_arrival'] = pd.to_datetime(df['actual_arrival'])
        df['delivery_delay_days'] = (df['actual_arrival'] - df['expected_delivery_date']).dt.days

        # Categorize failures
        failures = df[df['delivery_delay_days'] > 0].copy()
        failures['failure_category'] = pd.cut(
            failures['delivery_delay_days'],
            bins=[0, 3, 7, 14, float('inf')],
            labels=['Minor (1-3 days)', 'Moderate (4-7 days)', 'Severe (8-14 days)', 'Critical (>14 days)']
        )

        failure_counts = failures['failure_category'].value_counts().to_dict()

        return {
            'total_failures': len(failures),
            'failure_rate_percent': round(len(failures) / len(df) * 100, 2) if len(df) > 0 else 0,
            'failures_by_category': failure_counts,
            'average_failure_days': round(failures['delivery_delay_days'].mean(), 1)
        }

    def calculate_procurement_cycle_time(self):
        """
        Calculate average procurement to delivery cycle time

        Returns:
            Dictionary with cycle time metrics
        """
        df = self.orders.merge(self.logistics, on='order_id', how='left')
        df['order_date'] = pd.to_datetime(df['order_date'])
        df['actual_arrival'] = pd.to_datetime(df['actual_arrival'])

        df['cycle_time_days'] = (df['actual_arrival'] - df['order_date']).dt.days

        completed_orders = df[df['actual_arrival'].notna()]

        avg_cycle_time = completed_orders['cycle_time_days'].mean()
        median_cycle_time = completed_orders['cycle_time_days'].median()
        min_cycle_time = completed_orders['cycle_time_days'].min()
        max_cycle_time = completed_orders['cycle_time_days'].max()

        return {
            'average_cycle_time_days': round(avg_cycle_time, 1) if not pd.isna(avg_cycle_time) else 0,
            'median_cycle_time_days': round(median_cycle_time, 1) if not pd.isna(median_cycle_time) else 0,
            'min_cycle_time_days': int(min_cycle_time) if not pd.isna(min_cycle_time) else 0,
            'max_cycle_time_days': int(max_cycle_time) if not pd.isna(max_cycle_time) else 0
        }

    def generate_kpi_report(self):
        """
        Generate comprehensive KPI report

        Returns:
            Dictionary with all KPIs
        """
        report = {
            'report_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'on_time_delivery': self.calculate_on_time_delivery_rate(),
            'inventory_turnover': self.calculate_inventory_turnover(),
            'service_level_failures': self.calculate_service_level_failures(),
            'procurement_cycle_time': self.calculate_procurement_cycle_time(),
            'supplier_performance': self.calculate_supplier_performance().to_dict('index')
        }

        return report

def main():
    """Example usage"""
    # Load sample data
    try:
        orders = pd.read_csv('data/sample_orders.csv')
        suppliers = pd.read_csv('data/sample_suppliers.csv')
        inventory = pd.read_csv('data/sample_inventory.csv')
        logistics = pd.read_csv('data/sample_logistics.csv')

        # Calculate KPIs
        calculator = SupplyChainKPICalculator(orders, suppliers, inventory, logistics)
        report = calculator.generate_kpi_report()

        # Print report
        print("\n" + "="*60)
        print("SUPPLY CHAIN KPI REPORT")
        print("="*60)
        print(f"\nReport Generated: {report['report_date']}")

        print("\n--- ON-TIME DELIVERY ---")
        for key, value in report['on_time_delivery'].items():
            print(f"{key}: {value}")

        print("\n--- INVENTORY TURNOVER ---")
        for key, value in report['inventory_turnover'].items():
            print(f"{key}: {value}")

        print("\n--- PROCUREMENT CYCLE TIME ---")
        for key, value in report['procurement_cycle_time'].items():
            print(f"{key}: {value}")

        print("\n" + "="*60)

    except FileNotFoundError as e:
        print(f"Error: Sample data files not found. {e}")
        print("Please run data generation script first.")

if __name__ == "__main__":
    main()
