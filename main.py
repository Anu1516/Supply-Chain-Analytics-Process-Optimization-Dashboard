"""
Main Script for Supply Chain Analytics Dashboard
Orchestrates data extraction, KPI calculation, alerts, and root cause analysis
"""

import pandas as pd
from src.data_extraction import ERPDataExtractor
from src.kpi_calculator import SupplyChainKPICalculator
from src.alert_system import SupplyChainAlertSystem
from src.root_cause_analysis import RootCauseAnalyzer
import json
from datetime import datetime
import os

def run_analytics_pipeline():
    """Run complete analytics pipeline"""

    print("\n" + "="*80)
    print("SUPPLY CHAIN ANALYTICS DASHBOARD - FULL PIPELINE")
    print("="*80)

    # Step 1: Load sample data (in production, this would extract from ERP)
    print("\n[Step 1] Loading data...")
    try:
        orders_df = pd.read_csv('data/sample_orders.csv')
        suppliers_df = pd.read_csv('data/sample_suppliers.csv')
        inventory_df = pd.read_csv('data/sample_inventory.csv')
        logistics_df = pd.read_csv('data/sample_logistics.csv')
        print(f"✓ Loaded {len(orders_df)} orders, {len(suppliers_df)} suppliers")
        print(f"✓ Loaded {len(inventory_df)} inventory items, {len(logistics_df)} shipments")
    except FileNotFoundError:
        print("✗ Sample data not found. Please run: python src/generate_sample_data.py")
        return

    # Step 2: Calculate KPIs
    print("\n[Step 2] Calculating KPIs...")
    kpi_calculator = SupplyChainKPICalculator(orders_df, suppliers_df, inventory_df, logistics_df)
    kpi_report = kpi_calculator.generate_kpi_report()

    print("\nKey Metrics:")
    print(f"  OTD Rate: {kpi_report['on_time_delivery']['otd_rate_percent']}%")
    print(f"  Inventory Turnover: {kpi_report['inventory_turnover']['inventory_turnover_ratio']}")
    print(f"  Avg Cycle Time: {kpi_report['procurement_cycle_time']['average_cycle_time_days']} days")

    # Step 3: Run Root Cause Analysis
    print("\n[Step 3] Running root cause analysis...")
    rca = RootCauseAnalyzer(orders_df, suppliers_df, logistics_df)
    rca_report = rca.generate_root_cause_report(inventory_df)

    delay_analysis = rca_report['delivery_delay_analysis']
    if 'total_delayed_orders' in delay_analysis:
        print(f"  Delayed Orders: {delay_analysis['total_delayed_orders']}")
        print(f"  Avg Delay: {delay_analysis['avg_delay_days']} days")

    # Step 4: Generate Alerts
    print("\n[Step 4] Generating alerts...")
    alert_system = SupplyChainAlertSystem()

    # Get supplier performance for alerts
    supplier_performance_df = pd.DataFrame.from_dict(
        kpi_report['supplier_performance'],
        orient='index'
    )

    alerts = alert_system.generate_alerts(
        kpi_report,
        inventory_df,
        orders_df,
        logistics_df,
        supplier_performance_df
    )

    print(f"  Generated {len(alerts)} alerts")
    if alerts:
        critical = len([a for a in alerts if a['severity'] == 'CRITICAL'])
        high = len([a for a in alerts if a['severity'] == 'HIGH'])
        print(f"  - Critical: {critical}, High: {high}")

    # Step 5: Save Reports
    print("\n[Step 5] Saving reports...")
    os.makedirs('reports', exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Save KPI report
    kpi_file = f'reports/kpi_report_{timestamp}.json'
    with open(kpi_file, 'w') as f:
        # Convert DataFrames to dict for JSON serialization
        kpi_report_copy = kpi_report.copy()
        json.dump(kpi_report_copy, f, indent=2, default=str)
    print(f"  ✓ KPI Report: {kpi_file}")

    # Save RCA report
    rca_file = f'reports/root_cause_analysis_{timestamp}.json'
    with open(rca_file, 'w') as f:
        json.dump(rca_report, f, indent=2, default=str)
    print(f"  ✓ RCA Report: {rca_file}")

    # Save alerts
    if alerts:
        alert_system.save_alerts_to_file(alerts)
        alert_system.print_alerts(alerts)

    # Step 6: Display Summary
    print("\n" + "="*80)
    print("PIPELINE EXECUTION COMPLETED SUCCESSFULLY")
    print("="*80)
    print("\nNext Steps:")
    print("  1. Open Power BI Desktop")
    print("  2. Load data from data/sample_*.csv files")
    print("  3. Create visualizations using KPI metrics")
    print("  4. Review alerts in data/alerts_log.json")
    print("  5. Explore Jupyter notebook: notebooks/analysis_exploration.ipynb")

    return {
        'kpi_report': kpi_report,
        'rca_report': rca_report,
        'alerts': alerts
    }

def quick_summary():
    """Generate quick summary of current state"""
    try:
        orders_df = pd.read_csv('data/sample_orders.csv')
        suppliers_df = pd.read_csv('data/sample_suppliers.csv')
        inventory_df = pd.read_csv('data/sample_inventory.csv')
        logistics_df = pd.read_csv('data/sample_logistics.csv')

        print("\n" + "="*60)
        print("QUICK SUMMARY")
        print("="*60)
        print(f"Total Orders: {len(orders_df)}")
        print(f"Total Suppliers: {len(suppliers_df)}")
        print(f"Inventory Items: {len(inventory_df)}")
        print(f"Shipments: {len(logistics_df)}")

        # Quick KPI
        kpi_calc = SupplyChainKPICalculator(orders_df, suppliers_df, inventory_df, logistics_df)
        otd = kpi_calc.calculate_on_time_delivery_rate()
        print(f"\nOn-Time Delivery Rate: {otd['otd_rate_percent']}%")

    except FileNotFoundError:
        print("Data not found. Run: python src/generate_sample_data.py")

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == 'summary':
        quick_summary()
    else:
        results = run_analytics_pipeline()
