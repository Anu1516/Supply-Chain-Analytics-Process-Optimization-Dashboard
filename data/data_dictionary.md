# Data Dictionary

## Orders Table

| Column Name | Data Type | Description |
|------------|-----------|-------------|
| order_id | String | Unique order identifier (e.g., ORD00001) |
| order_date | Date | Date when order was placed |
| supplier_id | String | Reference to supplier (foreign key) |
| product_id | String | Product identifier |
| quantity | Integer | Quantity ordered |
| unit_price | Decimal | Price per unit |
| total_amount | Decimal | Total order value (quantity × unit_price) |
| expected_delivery_date | Date | Expected delivery date |
| actual_delivery_date | Date | Actual delivery date (NULL if not delivered) |
| status | String | Order status (Completed, In Transit, Processing, Delivered) |
| warehouse_id | String | Destination warehouse identifier |

## Suppliers Table

| Column Name | Data Type | Description |
|------------|-----------|-------------|
| supplier_id | String | Unique supplier identifier (e.g., SUP0001) |
| supplier_name | String | Supplier business name |
| country | String | Supplier country location |
| category | String | Supplier category (Raw Materials, Components, etc.) |
| rating | Decimal | Supplier rating (1.0 - 5.0) |
| contract_start_date | Date | Contract start date |
| contract_end_date | Date | Contract expiration date |
| payment_terms | String | Payment terms (Net 30, Net 45, etc.) |
| lead_time_days | Integer | Standard lead time in days |

## Inventory Table

| Column Name | Data Type | Description |
|------------|-----------|-------------|
| product_id | String | Product identifier |
| warehouse_id | String | Warehouse location identifier |
| current_stock | Integer | Current stock quantity |
| reorder_point | Integer | Reorder threshold quantity |
| max_stock_level | Integer | Maximum stock level |
| last_stock_date | Date | Last stock update date |
| stock_value | Decimal | Total value of stock (quantity × unit value) |
| stock_age_days | Integer | Average age of stock in days |

## Logistics/Shipments Table

| Column Name | Data Type | Description |
|------------|-----------|-------------|
| shipment_id | String | Unique shipment identifier (e.g., SHIP00001) |
| order_id | String | Reference to order (foreign key) |
| carrier_name | String | Shipping carrier name |
| tracking_number | String | Carrier tracking number |
| ship_date | Date | Date shipment departed |
| estimated_arrival | Date | Estimated arrival date |
| actual_arrival | Date | Actual arrival date (NULL if in transit) |
| origin_location | String | Shipment origin |
| destination_location | String | Shipment destination |
| shipment_cost | Decimal | Shipping cost |
| status | String | Shipment status (Delivered, In Transit, Delayed) |

## Calculated Metrics

### On-Time Delivery (OTD)
- **Formula**: (Orders delivered on or before expected date / Total delivered orders) × 100
- **Target**: ≥ 95%

### Inventory Turnover Ratio
- **Formula**: Cost of Goods Sold / Average Inventory Value
- **Target**: ≥ 4.0 (varies by industry)

### Days Inventory Outstanding (DIO)
- **Formula**: 365 / Inventory Turnover Ratio
- **Lower is better**: Indicates faster inventory movement

### Procurement Cycle Time
- **Formula**: Average days from order date to actual delivery
- **Components**:
  - Order to Ship: Days from order to shipment
  - Ship to Delivery: Days from shipment to delivery

### Supplier Performance Score
- **Formula**: (OTD Rate × 0.5) + (Rating × 10)
- **Range**: 0-100
- **Target**: ≥ 50
