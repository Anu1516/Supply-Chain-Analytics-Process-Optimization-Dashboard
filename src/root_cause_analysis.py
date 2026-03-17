"""
Root Cause Analysis Module
Framework for identifying bottlenecks in procurement-to-delivery process
"""

import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

class RootCauseAnalyzer:
    """Analyze root causes of supply chain bottlenecks"""

    def __init__(self, orders_df, suppliers_df, logistics_df):
        """
        Initialize root cause analyzer

        Args:
            orders_df: Orders DataFrame
            suppliers_df: Suppliers DataFrame
            logistics_df: Logistics DataFrame
        """
        self.orders = orders_df
        self.suppliers = suppliers_df
        self.logistics = logistics_df
        self.analysis_results = {}

    def analyze_delivery_delays(self):
        """
        Analyze root causes of delivery delays

        Returns:
            Dictionary with delay analysis
        """
        df = self.orders.merge(self.logistics, on='order_id', how='left')
        df = df.merge(self.suppliers, on='supplier_id', how='left')

        df['expected_delivery_date'] = pd.to_datetime(df['expected_delivery_date'])
        df['actual_arrival'] = pd.to_datetime(df['actual_arrival'])
        df['delivery_delay_days'] = (df['actual_arrival'] - df['expected_delivery_date']).dt.days

        # Filter delayed orders
        delayed = df[df['delivery_delay_days'] > 0].copy()

        if delayed.empty:
            return {'message': 'No delayed orders found'}

        # Analyze by supplier
        by_supplier = delayed.groupby('supplier_name').agg({
            'delivery_delay_days': ['count', 'mean', 'max'],
            'order_id': 'count'
        }).round(2)
        by_supplier.columns = ['delay_count', 'avg_delay_days', 'max_delay_days', 'total_orders']
        by_supplier['delay_rate_percent'] = (by_supplier['delay_count'] / by_supplier['total_orders'] * 100).round(2)
        by_supplier = by_supplier.sort_values('avg_delay_days', ascending=False)

        # Analyze by country/region
        by_country = delayed.groupby('country').agg({
            'delivery_delay_days': ['count', 'mean'],
            'order_id': 'count'
        }).round(2)
        by_country.columns = ['delay_count', 'avg_delay_days', 'total_orders']
        by_country = by_country.sort_values('avg_delay_days', ascending=False)

        # Analyze by product category
        by_category = delayed.groupby('category').agg({
            'delivery_delay_days': ['count', 'mean'],
            'order_id': 'count'
        }).round(2)
        by_category.columns = ['delay_count', 'avg_delay_days', 'total_orders']
        by_category = by_category.sort_values('avg_delay_days', ascending=False)

        return {
            'total_delayed_orders': len(delayed),
            'total_delay_days': int(delayed['delivery_delay_days'].sum()),
            'avg_delay_days': round(delayed['delivery_delay_days'].mean(), 2),
            'by_supplier': by_supplier.head(10).to_dict('index'),
            'by_country': by_country.to_dict('index'),
            'by_category': by_category.to_dict('index')
        }

    def analyze_procurement_bottlenecks(self):
        """
        Identify bottlenecks in procurement process

        Returns:
            Dictionary with bottleneck analysis
        """
        df = self.orders.merge(self.logistics, on='order_id', how='left')
        df['order_date'] = pd.to_datetime(df['order_date'])
        df['ship_date'] = pd.to_datetime(df['ship_date'])
        df['actual_arrival'] = pd.to_datetime(df['actual_arrival'])

        # Calculate different cycle time components
        df['order_to_ship_days'] = (df['ship_date'] - df['order_date']).dt.days
        df['ship_to_delivery_days'] = (df['actual_arrival'] - df['ship_date']).dt.days
        df['total_cycle_time'] = (df['actual_arrival'] - df['order_date']).dt.days

        # Identify bottlenecks
        avg_order_to_ship = df['order_to_ship_days'].mean()
        avg_ship_to_delivery = df['ship_to_delivery_days'].mean()

        # Find orders with excessive time in each stage
        bottleneck_order_to_ship = df[df['order_to_ship_days'] > avg_order_to_ship * 1.5]
        bottleneck_ship_to_delivery = df[df['ship_to_delivery_days'] > avg_ship_to_delivery * 1.5]

        return {
            'avg_order_to_ship_days': round(avg_order_to_ship, 2),
            'avg_ship_to_delivery_days': round(avg_ship_to_delivery, 2),
            'bottleneck_order_processing_count': len(bottleneck_order_to_ship),
            'bottleneck_logistics_count': len(bottleneck_ship_to_delivery),
            'recommendation': self._generate_bottleneck_recommendations(avg_order_to_ship, avg_ship_to_delivery)
        }

    def analyze_inventory_issues(self, inventory_df):
        """
        Analyze inventory-related issues

        Args:
            inventory_df: Inventory DataFrame

        Returns:
            Dictionary with inventory analysis
        """
        # Stock out analysis
        stock_outs = inventory_df[inventory_df['current_stock'] <= 0]

        # Below reorder point
        below_reorder = inventory_df[
            (inventory_df['current_stock'] > 0) &
            (inventory_df['current_stock'] < inventory_df['reorder_point'])
        ]

        # Excess stock
        excess_stock = inventory_df[inventory_df['stock_age_days'] > 90]

        # Overstocked
        overstocked = inventory_df[inventory_df['current_stock'] > inventory_df['max_stock_level']]

        return {
            'stock_out_count': len(stock_outs),
            'stock_out_value': round(stock_outs['stock_value'].sum(), 2),
            'below_reorder_count': len(below_reorder),
            'below_reorder_value': round(below_reorder['stock_value'].sum(), 2),
            'excess_stock_count': len(excess_stock),
            'excess_stock_value': round(excess_stock['stock_value'].sum(), 2),
            'overstocked_count': len(overstocked),
            'overstocked_value': round(overstocked['stock_value'].sum(), 2),
            'recommendations': self._generate_inventory_recommendations(stock_outs, excess_stock, overstocked)
        }

    def _generate_bottleneck_recommendations(self, avg_order_to_ship, avg_ship_to_delivery):
        """Generate recommendations based on bottleneck analysis"""
        recommendations = []

        if avg_order_to_ship > 3:
            recommendations.append("Order processing time is high. Consider automating approval workflows.")

        if avg_ship_to_delivery > 7:
            recommendations.append("Logistics delivery time is high. Review carrier contracts and consider alternative options.")

        if not recommendations:
            recommendations.append("Cycle times are within acceptable ranges. Continue monitoring.")

        return recommendations

    def _generate_inventory_recommendations(self, stock_outs, excess_stock, overstocked):
        """Generate inventory recommendations"""
        recommendations = []

        if len(stock_outs) > 0:
            recommendations.append(f"Critical: {len(stock_outs)} stock-outs detected. Implement safety stock policies.")

        if len(excess_stock) > 10:
            recommendations.append(f"Warning: {len(excess_stock)} slow-moving items. Consider clearance or return to supplier.")

        if len(overstocked) > 5:
            recommendations.append(f"Alert: {len(overstocked)} overstocked items. Review reorder quantities.")

        if not recommendations:
            recommendations.append("Inventory levels are well-balanced. Continue current practices.")

        return recommendations

    def perform_pareto_analysis(self):
        """
        Perform Pareto analysis (80/20 rule) on delayed orders

        Returns:
            DataFrame with Pareto analysis results
        """
        df = self.orders.merge(self.logistics, on='order_id', how='left')
        df = df.merge(self.suppliers, on='supplier_id', how='left')

        df['expected_delivery_date'] = pd.to_datetime(df['expected_delivery_date'])
        df['actual_arrival'] = pd.to_datetime(df['actual_arrival'])
        df['delivery_delay_days'] = (df['actual_arrival'] - df['expected_delivery_date']).dt.days

        # Filter delayed orders
        delayed = df[df['delivery_delay_days'] > 0].copy()

        if delayed.empty:
            return pd.DataFrame()

        # Group by supplier and calculate cumulative delay
        pareto = delayed.groupby('supplier_name').agg({
            'delivery_delay_days': 'sum',
            'order_id': 'count'
        }).rename(columns={'delivery_delay_days': 'total_delay_days', 'order_id': 'order_count'})

        pareto = pareto.sort_values('total_delay_days', ascending=False)

        # Calculate cumulative percentages
        pareto['cumulative_delay'] = pareto['total_delay_days'].cumsum()
        pareto['cumulative_delay_percent'] = (pareto['cumulative_delay'] / pareto['total_delay_days'].sum() * 100).round(2)

        # Identify 80% contributors
        pareto['is_80_percent'] = pareto['cumulative_delay_percent'] <= 80

        return pareto

    def generate_root_cause_report(self, inventory_df):
        """
        Generate comprehensive root cause analysis report

        Args:
            inventory_df: Inventory DataFrame

        Returns:
            Dictionary with complete analysis
        """
        report = {
            'timestamp': datetime.now().isoformat(),
            'delivery_delay_analysis': self.analyze_delivery_delays(),
            'procurement_bottlenecks': self.analyze_procurement_bottlenecks(),
            'inventory_analysis': self.analyze_inventory_issues(inventory_df),
            'pareto_analysis': self.perform_pareto_analysis().to_dict('index') if not self.perform_pareto_analysis().empty else {}
        }

        self.analysis_results = report
        return report

    def print_report(self, report=None):
        """Print root cause analysis report"""
        if report is None:
            report = self.analysis_results

        print("\n" + "="*80)
        print("ROOT CAUSE ANALYSIS REPORT")
        print("="*80)
        print(f"Generated: {report['timestamp']}\n")

        print("--- DELIVERY DELAY ANALYSIS ---")
        delay_analysis = report['delivery_delay_analysis']
        if 'message' in delay_analysis:
            print(delay_analysis['message'])
        else:
            print(f"Total Delayed Orders: {delay_analysis['total_delayed_orders']}")
            print(f"Average Delay: {delay_analysis['avg_delay_days']} days")

            if delay_analysis['by_supplier']:
                print("\nTop Suppliers by Delay:")
                for supplier, metrics in list(delay_analysis['by_supplier'].items())[:5]:
                    print(f"  {supplier}: {metrics['avg_delay_days']} days avg")

        print("\n--- PROCUREMENT BOTTLENECKS ---")
        bottlenecks = report['procurement_bottlenecks']
        print(f"Avg Order to Ship: {bottlenecks['avg_order_to_ship_days']} days")
        print(f"Avg Ship to Delivery: {bottlenecks['avg_ship_to_delivery_days']} days")
        print("\nRecommendations:")
        for rec in bottlenecks['recommendation']:
            print(f"  - {rec}")

        print("\n--- INVENTORY ANALYSIS ---")
        inventory = report['inventory_analysis']
        print(f"Stock Outs: {inventory['stock_out_count']}")
        print(f"Excess Stock Items: {inventory['excess_stock_count']}")
        print("\nRecommendations:")
        for rec in inventory['recommendations']:
            print(f"  - {rec}")

        print("\n" + "="*80)

if __name__ == "__main__":
    print("Root Cause Analysis Module")
    print("Load data and run analysis")
