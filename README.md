# Supply Chain Analytics & Process Optimization Dashboard

An end-to-end supply chain analytics dashboard built with Power BI and Python to track key performance indicators including on-time delivery, inventory turnover, and supplier performance metrics.

## Features

- **KPI Tracking**: Monitor on-time delivery, inventory turnover, and supplier performance
- **SQL-Based Data Extraction**: Automated data extraction from ERP systems
- **Daily Reporting**: Automated daily reports on logistics operations and service level failures
- **Root Cause Analysis**: Framework for identifying bottlenecks in procurement-to-delivery process
- **Automated Alerts**: Python and Power BI workflows for supply chain exception management

## Technologies Used

- **Python**: Data processing, automation, and alert generation
- **SQL**: Data extraction from ERP systems
- **Power BI**: Interactive dashboards and visualizations
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computations
- **matplotlib/plotly**: Additional visualizations

## Project Structure

```
Supply-Chain-Analytics-Process-Optimization-Dashboard/
├── data/
│   ├── sample_data.csv
│   └── data_dictionary.md
├── src/
│   ├── data_extraction.py
│   ├── kpi_calculator.py
│   ├── alert_system.py
│   └── root_cause_analysis.py
├── dashboards/
│   └── supply_chain_dashboard.pbix
├── notebooks/
│   └── analysis_exploration.ipynb
├── requirements.txt
└── README.md
```

## Installation

```bash
# Clone the repository
git clone https://github.com/anuchandrashekar/Supply-Chain-Analytics-Process-Optimization-Dashboard.git

# Navigate to project directory
cd Supply-Chain-Analytics-Process-Optimization-Dashboard

# Install required packages
pip install -r requirements.txt
```

## Usage

### 1. Data Extraction
```python
python src/data_extraction.py
```

### 2. Calculate KPIs
```python
python src/kpi_calculator.py
```

### 3. Run Alert System
```python
python src/alert_system.py
```

### 4. Root Cause Analysis
```python
python src/root_cause_analysis.py
```

## Key Metrics

- **On-Time Delivery Rate**: Percentage of orders delivered on time
- **Inventory Turnover**: How many times inventory is sold/used in a period
- **Supplier Performance Score**: Composite score based on quality, delivery, and cost
- **Service Level Failures**: Count and analysis of service failures
- **Procurement-to-Delivery Cycle Time**: Average time from order to delivery

## Dashboard Screenshots

The Power BI dashboard includes:
- Executive summary with key metrics
- Supplier performance comparison
- Delivery performance trends
- Inventory turnover analysis
- Root cause analysis visualizations

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

MIT

## Author

Anu Chandrashekar
- Email: anuchandrashekar7579@gmail.com
- LinkedIn: [linkedin.com/in/anu-chandrashekar-07496b211](https://www.linkedin.com/in/anu-chandrashekar-07496b211)
