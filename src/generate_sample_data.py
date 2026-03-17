"""Generate Sample Procurement Data"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_procurement_data():
    np.random.seed(42)
    random.seed(42)

    categories = ['Electronics', 'Office Supplies', 'Raw Materials', 'Services']
    vendors = [f'VEN{i:03d}' for i in range(1, 21)]

    data = []
    for i in range(500):
        po_date = datetime(2023, 1, 1) + timedelta(days=random.randint(0, 365))
        delivery_date = po_date + timedelta(days=random.randint(5, 30))
        expected_date = po_date + timedelta(days=14)

        data.append({
            'po_number': f'PO{i+1:05d}',
            'vendor_id': random.choice(vendors),
            'vendor_name': f'Vendor {random.choice(vendors)}',
            'category': random.choice(categories),
            'amount': round(random.uniform(1000, 50000), 2),
            'quantity': random.randint(10, 1000),
            'unit_price': round(random.uniform(10, 100), 2),
            'po_date': po_date.strftime('%Y-%m-%d'),
            'expected_delivery': expected_date.strftime('%Y-%m-%d'),
            'actual_delivery': delivery_date.strftime('%Y-%m-%d'),
            'days_late': (delivery_date - expected_date).days,
            'quality_score': round(random.uniform(60, 100), 1)
        })

    df = pd.DataFrame(data)
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/procurement_data.csv', index=False)
    print(f"Generated {len(df)} procurement records")
    return df

if __name__ == "__main__":
    generate_procurement_data()
