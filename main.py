"""Main script for Procurement Analytics"""
import sys, os
sys.path.append(os.path.dirname(__file__))
from src.spend_analyzer import SpendAnalyzer
from src.supplier_performance import SupplierPerformance
from src.generate_sample_data import generate_procurement_data

def main():
    print("=" * 80)
    print("PROCUREMENT DATA ANALYTICS & SPEND ANALYSIS")
    print("=" * 80)

    print("\n[1/3] Generating sample data...")
    generate_procurement_data()

    print("\n[2/3] Analyzing spend...")
    analyzer = SpendAnalyzer('data/procurement_data.csv')
    print("\nSpend by Category:")
    print(analyzer.analyze_spend_by_category())

    print("\n[3/3] Evaluating supplier performance...")
    perf = SupplierPerformance('data/procurement_data.csv')
    print("\nTop Suppliers:")
    print(perf.rank_suppliers().head(10))

    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()
