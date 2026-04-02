import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
import os

class Reporting:

    def __init__(self,
                 mart_path="data/information_mart",
                 output_path="data/visualizations"):
        self.mart_path   = mart_path
        self.output_path = output_path
        os.makedirs(self.output_path, exist_ok=True)

        self.fact         = pd.read_csv(f"{mart_path}/fact_sales.csv")
        self.dim_date     = pd.read_csv(f"{mart_path}/dim_date.csv")
        self.dim_product  = pd.read_csv(f"{mart_path}/dim_product.csv")
        self.dim_store    = pd.read_csv(f"{mart_path}/dim_store.csv")
        self.dim_customer = pd.read_csv(f"{mart_path}/dim_customer.csv")

        sns.set_theme(style="whitegrid", palette="muted")
        plt.rcParams['figure.dpi'] = 150

    def chart_sales_over_time(self):
        df = self.fact.merge(self.dim_date, on='date_id')
        df['year_month'] = df['year'].astype(str) + '-' + df['month'].astype(str).str.zfill(2)
        monthly = df.groupby('year_month')['total_price'].sum().reset_index().sort_values('year_month')

        fig, ax = plt.subplots(figsize=(12, 5))
        ax.plot(monthly['year_month'], monthly['total_price'],
                color='#534AB7', linewidth=2.5, marker='o', markersize=5)
        ax.fill_between(monthly['year_month'], monthly['total_price'],
                        alpha=0.1, color='#534AB7')
        ax.set_title('Sales Over Time', fontsize=14, fontweight='bold', pad=15)
        ax.set_xlabel('Month')
        ax.set_ylabel('Total Sales ($)')
        ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x:,.0f}'))
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(f"{self.output_path}/1_sales_over_time.png")
        plt.close()
        print("  ✓ Chart 1: Sales Over Time")

    def chart_top_products(self, top_n=10):
        df = self.fact.merge(self.dim_product, on='product_id')
        top = (df.groupby('product_name')['quantity']
                 .sum()
                 .reset_index()
                 .sort_values('quantity', ascending=True)
                 .tail(top_n))

        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.barh(top['product_name'], top['quantity'],
                       color='#1D9E75', edgecolor='none', height=0.6)
        for bar, val in zip(bars, top['quantity']):
            ax.text(bar.get_width() + 2, bar.get_y() + bar.get_height()/2,
                    f'{int(val)}', va='center', fontsize=10)
        ax.set_title(f'Top {top_n} Best Selling Products', fontsize=14,
                     fontweight='bold', pad=15)
        ax.set_xlabel('Units Sold')
        plt.tight_layout()
        plt.savefig(f"{self.output_path}/2_top_products.png")
        plt.close()
        print("  ✓ Chart 2: Top Products")

    def chart_customer_segmentation(self, top_n=5):
        df = self.fact.merge(self.dim_customer, on='customer_id')
        by_state = (df.groupby('state')['customer_id']
                      .nunique()
                      .reset_index()
                      .rename(columns={'customer_id': 'customers'})
                      .sort_values('customers', ascending=False))
        top    = by_state.head(top_n)
        others = pd.DataFrame([{'state': 'Others',
                                 'customers': by_state.tail(-top_n)['customers'].sum()}])
        data   = pd.concat([top, others])
        colors = ['#534AB7','#1D9E75','#D85A30','#BA7517','#888780','#B4B2A9']

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.pie(data['customers'], labels=data['state'], autopct='%1.1f%%',
               colors=colors[:len(data)], startangle=140,
               wedgeprops={'edgecolor': 'white', 'linewidth': 2})
        ax.set_title('Customer Segmentation by State', fontsize=14,
                     fontweight='bold', pad=15)
        plt.tight_layout()
        plt.savefig(f"{self.output_path}/3_customer_segmentation.png")
        plt.close()
        print("  ✓ Chart 3: Customer Segmentation")

    def chart_revenue_by_store(self):
        df = (self.fact
              .merge(self.dim_store, on='store_id')
              .merge(self.dim_date,  on='date_id'))
        pivot = (df.groupby(['store_name', 'year'])['total_price']
                   .sum()
                   .unstack(fill_value=0))

        fig, ax = plt.subplots(figsize=(10, 6))
        pivot.plot(kind='bar', ax=ax, colormap='Purples',
                   edgecolor='none', width=0.6)
        ax.set_title('Revenue by Store per Year', fontsize=14,
                     fontweight='bold', pad=15)
        ax.set_xlabel('Store')
        ax.set_ylabel('Revenue ($)')
        ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x:,.0f}'))
        plt.xticks(rotation=20, ha='right')
        plt.legend(title='Year')
        plt.tight_layout()
        plt.savefig(f"{self.output_path}/4_revenue_by_store.png")
        plt.close()
        print("  ✓ Chart 4: Revenue by Store")

    def run(self):
        print("\n📊 Generating Reports...")
        print("=" * 40)
        self.chart_sales_over_time()
        self.chart_top_products()
        self.chart_customer_segmentation()
        self.chart_revenue_by_store()
        print("=" * 40)
        print(f"✅ All charts saved to: {self.output_path}/")