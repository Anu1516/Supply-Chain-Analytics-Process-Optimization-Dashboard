"""
Data Extraction Module for Supply Chain Analytics
Extracts data from ERP systems using SQL queries
"""

import pandas as pd
import sqlalchemy
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ERPDataExtractor:
    """Extract data from ERP systems for supply chain analytics"""

    def __init__(self):
        """Initialize database connection"""
        # In production, these would come from environment variables
        self.connection_string = os.getenv('ERP_CONNECTION_STRING', 'sqlite:///data/erp_sample.db')
        self.engine = sqlalchemy.create_engine(self.connection_string)

    def extract_orders_data(self, start_date=None, end_date=None):
        """
        Extract orders data from ERP system

        Args:
            start_date: Start date for data extraction (default: 30 days ago)
            end_date: End date for data extraction (default: today)

        Returns:
            DataFrame with orders data
        """
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')

        query = f"""
        SELECT
            order_id,
            order_date,
            supplier_id,
            product_id,
            quantity,
            unit_price,
            total_amount,
            expected_delivery_date,
            actual_delivery_date,
            status,
            warehouse_id
        FROM orders
        WHERE order_date BETWEEN '{start_date}' AND '{end_date}'
        """

        try:
            df = pd.read_sql(query, self.engine)
            print(f"Extracted {len(df)} orders from {start_date} to {end_date}")
            return df
        except Exception as e:
            print(f"Error extracting orders data: {e}")
            return pd.DataFrame()

    def extract_supplier_data(self):
        """
        Extract supplier master data

        Returns:
            DataFrame with supplier information
        """
        query = """
        SELECT
            supplier_id,
            supplier_name,
            country,
            category,
            rating,
            contract_start_date,
            contract_end_date,
            payment_terms,
            lead_time_days
        FROM suppliers
        """

        try:
            df = pd.read_sql(query, self.engine)
            print(f"Extracted {len(df)} supplier records")
            return df
        except Exception as e:
            print(f"Error extracting supplier data: {e}")
            return pd.DataFrame()

    def extract_inventory_data(self):
        """
        Extract inventory data

        Returns:
            DataFrame with inventory levels
        """
        query = """
        SELECT
            product_id,
            warehouse_id,
            current_stock,
            reorder_point,
            max_stock_level,
            last_stock_date,
            stock_value,
            stock_age_days
        FROM inventory
        """

        try:
            df = pd.read_sql(query, self.engine)
            print(f"Extracted {len(df)} inventory records")
            return df
        except Exception as e:
            print(f"Error extracting inventory data: {e}")
            return pd.DataFrame()

    def extract_logistics_data(self, start_date=None, end_date=None):
        """
        Extract logistics and shipment data

        Args:
            start_date: Start date for data extraction
            end_date: End date for data extraction

        Returns:
            DataFrame with logistics data
        """
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')

        query = f"""
        SELECT
            shipment_id,
            order_id,
            carrier_name,
            tracking_number,
            ship_date,
            estimated_arrival,
            actual_arrival,
            origin_location,
            destination_location,
            shipment_cost,
            status
        FROM shipments
        WHERE ship_date BETWEEN '{start_date}' AND '{end_date}'
        """

        try:
            df = pd.read_sql(query, self.engine)
            print(f"Extracted {len(df)} shipment records")
            return df
        except Exception as e:
            print(f"Error extracting logistics data: {e}")
            return pd.DataFrame()

    def save_extracted_data(self, output_dir='data/extracted'):
        """
        Extract all data and save to CSV files

        Args:
            output_dir: Directory to save extracted data
        """
        os.makedirs(output_dir, exist_ok=True)

        # Extract all data
        orders_df = self.extract_orders_data()
        supplier_df = self.extract_supplier_data()
        inventory_df = self.extract_inventory_data()
        logistics_df = self.extract_logistics_data()

        # Save to CSV
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        if not orders_df.empty:
            orders_df.to_csv(f'{output_dir}/orders_{timestamp}.csv', index=False)
            print(f"Saved orders data to {output_dir}/orders_{timestamp}.csv")

        if not supplier_df.empty:
            supplier_df.to_csv(f'{output_dir}/suppliers_{timestamp}.csv', index=False)
            print(f"Saved supplier data to {output_dir}/suppliers_{timestamp}.csv")

        if not inventory_df.empty:
            inventory_df.to_csv(f'{output_dir}/inventory_{timestamp}.csv', index=False)
            print(f"Saved inventory data to {output_dir}/inventory_{timestamp}.csv")

        if not logistics_df.empty:
            logistics_df.to_csv(f'{output_dir}/logistics_{timestamp}.csv', index=False)
            print(f"Saved logistics data to {output_dir}/logistics_{timestamp}.csv")

        return {
            'orders': orders_df,
            'suppliers': supplier_df,
            'inventory': inventory_df,
            'logistics': logistics_df
        }

if __name__ == "__main__":
    # Example usage
    extractor = ERPDataExtractor()
    data = extractor.save_extracted_data()
    print(f"\nData extraction completed successfully!")
    print(f"Orders: {len(data['orders'])} records")
    print(f"Suppliers: {len(data['suppliers'])} records")
    print(f"Inventory: {len(data['inventory'])} records")
    print(f"Logistics: {len(data['logistics'])} records")
