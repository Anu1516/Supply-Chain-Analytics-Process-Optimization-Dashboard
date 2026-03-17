# Quick Start Guide

## Setup

1. **Clone the repository**
```bash
git clone https://github.com/anuchandrashekar/Supply-Chain-Analytics-Process-Optimization-Dashboard.git
cd Supply-Chain-Analytics-Process-Optimization-Dashboard
```

2. **Create virtual environment** (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

## Generate Sample Data

```bash
python src/generate_sample_data.py
```

This will create sample datasets in the `data/` directory:
- `sample_orders.csv`
- `sample_suppliers.csv`
- `sample_inventory.csv`
- `sample_logistics.csv`

## Run the Complete Pipeline

```bash
python main.py
```

This will:
1. Load data from CSV files
2. Calculate all KPIs
3. Run root cause analysis
4. Generate alerts
5. Save reports to `reports/` directory

## Quick Summary

For a quick overview without running the full pipeline:

```bash
python main.py summary
```

## Individual Module Usage

### Calculate KPIs Only
```python
from src.kpi_calculator import SupplyChainKPICalculator
import pandas as pd

orders = pd.read_csv('data/sample_orders.csv')
suppliers = pd.read_csv('data/sample_suppliers.csv')
inventory = pd.read_csv('data/sample_inventory.csv')
logistics = pd.read_csv('data/sample_logistics.csv')

calculator = SupplyChainKPICalculator(orders, suppliers, inventory, logistics)
report = calculator.generate_kpi_report()
```

### Generate Alerts Only
```python
from src.alert_system import SupplyChainAlertSystem

alert_system = SupplyChainAlertSystem()
alerts = alert_system.generate_alerts(kpi_data, inventory_df, orders_df, logistics_df, supplier_perf_df)
alert_system.print_alerts(alerts)
```

### Root Cause Analysis Only
```python
from src.root_cause_analysis import RootCauseAnalyzer

rca = RootCauseAnalyzer(orders_df, suppliers_df, logistics_df)
report = rca.generate_root_cause_report(inventory_df)
rca.print_report()
```

## Jupyter Notebook Analysis

For interactive analysis and visualizations:

```bash
jupyter notebook notebooks/analysis_exploration.ipynb
```

## Power BI Dashboard

1. Open Power BI Desktop
2. Import data from `data/sample_*.csv` files
3. Create relationships:
   - `orders.supplier_id` → `suppliers.supplier_id`
   - `orders.order_id` → `logistics.order_id`
   - `inventory.product_id` → `orders.product_id`
4. Use calculated KPIs from the reports as reference
5. Build visualizations

## Project Structure

```
Supply-Chain-Analytics-Process-Optimization-Dashboard/
├── data/                    # Sample data files
│   ├── sample_orders.csv
│   ├── sample_suppliers.csv
│   ├── sample_inventory.csv
│   ├── sample_logistics.csv
│   └── data_dictionary.md
├── src/                     # Source code
│   ├── data_extraction.py
│   ├── kpi_calculator.py
│   ├── alert_system.py
│   ├── root_cause_analysis.py
│   └── generate_sample_data.py
├── notebooks/               # Jupyter notebooks
│   └── analysis_exploration.ipynb
├── reports/                 # Generated reports (created at runtime)
├── dashboards/              # Power BI files (user-created)
├── main.py                  # Main pipeline script
├── requirements.txt         # Python dependencies
├── QUICK_START.md          # This file
└── README.md               # Project documentation
```

## Next Steps

1. Explore the Jupyter notebook for interactive analysis
2. Create Power BI dashboards
3. Customize alert thresholds in `config/alert_config.json`
4. Adapt data extraction module for your ERP system
5. Schedule automated runs using cron/Task Scheduler

## Troubleshooting

**Issue**: Module import errors
**Solution**: Make sure you're in the project root directory and virtual environment is activated

**Issue**: Sample data not found
**Solution**: Run `python src/generate_sample_data.py` first

**Issue**: Permission denied on file creation
**Solution**: Ensure you have write permissions in the project directory

## Support

For issues or questions:
- Email: anuchandrashekar7579@gmail.com
- LinkedIn: [Anu Chandrashekar](https://www.linkedin.com/in/anu-chandrashekar-07496b211)
