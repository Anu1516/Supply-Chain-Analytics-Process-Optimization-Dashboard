"""Spend Analysis Module"""
import pandas as pd
import numpy as np

class SpendAnalyzer:
    def __init__(self, data_path):
        self.df = pd.read_csv(data_path)

    def analyze_spend_by_category(self):
        """Analyze spend by category"""
        return self.df.groupby('category')['amount'].agg(['sum', 'mean', 'count'])

    def identify_top_vendors(self, n=10):
        """Identify top vendors by spend"""
        return self.df.groupby('vendor_name')['amount'].sum().nlargest(n)

    def calculate_savings_opportunity(self):
        """Calculate potential savings"""
        avg_price = self.df.groupby('category')['unit_price'].mean()
        savings = []
        for idx, row in self.df.iterrows():
            cat_avg = avg_price[row['category']]
            if row['unit_price'] > cat_avg * 1.1:
                potential = (row['unit_price'] - cat_avg) * row['quantity']
                savings.append({'po_number': row['po_number'], 'savings': potential})
        return pd.DataFrame(savings)

if __name__ == "__main__":
    print("Spend Analyzer Module")
