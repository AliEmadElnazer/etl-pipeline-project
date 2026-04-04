import pandas as pd
import matplotlib.pyplot as plt

# load data
df = pd.read_csv("data/staging_2/sales_dataset.csv")

# ---------------------------
# 1. Sales Over Time
# ---------------------------
df["order_date"] = pd.to_datetime(df["order_date"])

sales_over_time = df.groupby(df["order_date"].dt.date)["price_egp"].sum()

plt.figure()
sales_over_time.plot()
plt.title("Sales Over Time")
plt.xlabel("Date")
plt.ylabel("Total Sales (EGP)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("data/mart/sales_over_time.png")
plt.close()

# ---------------------------
# 2. Top Products
# ---------------------------
top_products = df.groupby("product_name")["price_egp"].sum().sort_values(ascending=False).head(10)

plt.figure()
top_products.plot(kind="bar")
plt.title("Top 10 Products")
plt.xlabel("Product")
plt.ylabel("Sales (EGP)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("data/mart/top_products.png")
plt.close()

# ---------------------------
# 3. Late Deliveries
# ---------------------------
late_counts = df["late_delivery"].value_counts()

plt.figure()
late_counts.plot(kind="bar")
plt.title("Late Deliveries Distribution")
plt.xlabel("Late Delivery")
plt.ylabel("Count")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("data/mart/late_deliveries.png")
plt.close()

print("📊 Visualizations Created Successfully")