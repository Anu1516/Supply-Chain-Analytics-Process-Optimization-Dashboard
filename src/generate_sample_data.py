"""
Generate Sample Data for Supply Chain Analytics Dashboard
Creates realistic sample datasets for demonstration purposes
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

def generate_suppliers(n=50):
    """Generate sample supplier data"""
    countries = ['USA', 'China', 'Germany', 'India', 'Japan', 'Mexico', 'Vietnam', 'Thailand']
    categories = ['Raw Materials', 'Components', 'Packaging', 'Equipment', 'Services']

    suppliers = []
    for i in range(1, n+1):
        supplier = {
            'supplier_id': f'SUP{i:04d}',
            'supplier_name': f'Supplier {i}',
            'country': random.choice(countries),
            'category': random.choice(categories),
            'rating': round(random.uniform(3.0, 5.0), 1),
            'contract_start_date': (datetime.now() - timedelta(days=random.randint(365, 1825))).strftime('%Y-%m-%d'),
            'contract_end_date': (datetime.now() + timedelta(days=random.randint(180, 730))).strftime('%Y-%m-%d'),
            'payment_terms': random.choice(['Net 30', 'Net 45', 'Net 60', 'Net 90']),
            'lead_time_days': random.randint(5, 30)
        }
        suppliers.append(supplier)

    return pd.DataFrame(suppliers)

def generate_orders(suppliers_df, n=500):
    """Generate sample order data"""
    statuses = ['Completed', 'In Transit', 'Processing', 'Delivered']
    warehouses = ['WH001', 'WH002', 'WH003', 'WH004', 'WH005']

    orders = []
    for i in range(1, n+1):
        order_date = datetime.now() - timedelta(days=random.randint(1, 90))
        supplier = suppliers_df.sample(1).iloc[0]
        lead_time = supplier['lead_time_days']

        expected_delivery = order_date + timedelta(days=lead_time)

        # 70% on-time, 30% delayed
        if random.random() < 0.7:
            actual_delivery = expected_delivery - timedelta(days=random.randint(0, 2))
        else:
            actual_delivery = expected_delivery + timedelta(days=random.randint(1, 15))

        # 10% of orders not yet delivered
        if random.random() < 0.1:
            actual_delivery_str = None
            status = 'In Transit'
        else:
            actual_delivery_str = actual_delivery.strftime('%Y-%m-%d')
            status = 'Delivered'

        quantity = random.randint(10, 500)
        unit_price = round(random.uniform(10, 1000), 2)

        order = {
            'order_id': f'ORD{i:05d}',
            'order_date': order_date.strftime('%Y-%m-%d'),
            'supplier_id': supplier['supplier_id'],
            'product_id': f'PROD{random.randint(1, 100):04d}',
            'quantity': quantity,
            'unit_price': unit_price,
            'total_amount': round(quantity * unit_price, 2),
            'expected_delivery_date': expected_delivery.strftime('%Y-%m-%d'),
            'actual_delivery_date': actual_delivery_str,
            'status': status,
            'warehouse_id': random.choice(warehouses)
        }
        orders.append(order)

    return pd.DataFrame(orders)

def generate_logistics(orders_df):
    """Generate sample logistics/shipment data"""
    carriers = ['FedEx', 'UPS', 'DHL', 'USPS', 'Local Carrier']
    statuses = ['Delivered', 'In Transit', 'Delayed']

    logistics = []
    for idx, order in orders_df.iterrows():
        order_date = pd.to_datetime(order['order_date'])
        ship_date = order_date + timedelta(days=random.randint(1, 3))

        if order['actual_delivery_date']:
            actual_arrival = pd.to_datetime(order['actual_delivery_date'])
            status = 'Delivered'
        else:
            actual_arrival = None
            status = random.choice(['In Transit', 'Delayed'])

        shipment = {
            'shipment_id': f'SHIP{idx+1:05d}',
            'order_id': order['order_id'],
            'carrier_name': random.choice(carriers),
            'tracking_number': f'TRK{random.randint(100000000, 999999999)}',
            'ship_date': ship_date.strftime('%Y-%m-%d'),
            'estimated_arrival': order['expected_delivery_date'],
            'actual_arrival': actual_arrival.strftime('%Y-%m-%d') if actual_arrival else None,
            'origin_location': f'City {random.randint(1, 20)}',
            'destination_location': order['warehouse_id'],
            'shipment_cost': round(random.uniform(50, 500), 2),
            'status': status
        }
        logistics.append(shipment)

    return pd.DataFrame(logistics)

def generate_inventory(n=200):
    """Generate sample inventory data"""
    warehouses = ['WH001', 'WH002', 'WH003', 'WH004', 'WH005']

    inventory = []
    for i in range(1, n+1):
        current_stock = random.randint(0, 1000)
        reorder_point = random.randint(50, 200)
        max_stock = reorder_point * 3
        unit_value = round(random.uniform(10, 500), 2)

        item = {
            'product_id': f'PROD{i:04d}',
            'warehouse_id': random.choice(warehouses),
            'current_stock': current_stock,
            'reorder_point': reorder_point,
            'max_stock_level': max_stock,
            'last_stock_date': (datetime.now() - timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d'),
            'stock_value': round(current_stock * unit_value, 2),
            'stock_age_days': random.randint(0, 180)
        }
        inventory.append(item)

    return pd.DataFrame(inventory)

def main():
    """Generate all sample datasets"""
    print("Generating sample data for Supply Chain Analytics Dashboard...")

    # Create data directory
    os.makedirs('data', exist_ok=True)

    # Generate datasets
    print("\n1. Generating suppliers data...")
    suppliers_df = generate_suppliers(50)
    suppliers_df.to_csv('data/sample_suppliers.csv', index=False)
    print(f"   Created {len(suppliers_df)} supplier records")

    print("\n2. Generating orders data...")
    orders_df = generate_orders(suppliers_df, 500)
    orders_df.to_csv('data/sample_orders.csv', index=False)
    print(f"   Created {len(orders_df)} order records")

    print("\n3. Generating logistics data...")
    logistics_df = generate_logistics(orders_df)
    logistics_df.to_csv('data/sample_logistics.csv', index=False)
    print(f"   Created {len(logistics_df)} shipment records")

    print("\n4. Generating inventory data...")
    inventory_df = generate_inventory(200)
    inventory_df.to_csv('data/sample_inventory.csv', index=False)
    print(f"   Created {len(inventory_df)} inventory records")

    print("\n" + "="*60)
    print("Sample data generation completed successfully!")
    print("="*60)
    print("\nFiles created:")
    print("  - data/sample_suppliers.csv")
    print("  - data/sample_orders.csv")
    print("  - data/sample_logistics.csv")
    print("  - data/sample_inventory.csv")
    print("\nYou can now run the KPI calculator and alert system.")

if __name__ == "__main__":
    main()
