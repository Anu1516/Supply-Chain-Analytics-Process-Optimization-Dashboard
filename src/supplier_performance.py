"""Supplier Performance Tracking"""
import pandas as pd

class SupplierPerformance:
    def __init__(self, data_path):
        self.df = pd.read_csv(data_path)

    def calculate_otd_rate(self, vendor_id):
        """Calculate on-time delivery rate"""
        vendor_data = self.df[self.df['vendor_id'] == vendor_id]
        if len(vendor_data) == 0:
            return 0
        otd_count = (vendor_data['days_late'] <= 0).sum()
        return (otd_count / len(vendor_data)) * 100

    def calculate_quality_score(self, vendor_id):
        """Calculate quality score"""
        vendor_data = self.df[self.df['vendor_id'] == vendor_id]
        if len(vendor_data) == 0:
            return 0
        return vendor_data['quality_score'].mean()

    def rank_suppliers(self):
        """Rank all suppliers"""
        vendors = self.df['vendor_id'].unique()
        rankings = []
        for vendor in vendors:
            rankings.append({
                'vendor_id': vendor,
                'otd_rate': self.calculate_otd_rate(vendor),
                'quality_score': self.calculate_quality_score(vendor),
                'total_spend': self.df[self.df['vendor_id'] == vendor]['amount'].sum()
            })
        return pd.DataFrame(rankings).sort_values('otd_rate', ascending=False)

if __name__ == "__main__":
    print("Supplier Performance Module")
