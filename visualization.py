import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------
# Load Data
# ---------------------------
df = pd.read_csv("data/staging_2/sales_dataset.csv")

# ---------------------------
# 1. Sales Over Time
# ---------------------------
df["order_date"] = pd.to_datetime(df["order_date"])

sales_over_time = df.groupby(df["order_date"].dt.date)["price_egp"].sum()

plt.figure(figsize=(10, 5))
sales_over_time.plot()

plt.title("Sales Over Time")
plt.xlabel("Date")
plt.ylabel("Total Sales (EGP)")
plt.xticks(rotation=45)

plt.grid(True)
plt.tight_layout()
plt.savefig("data/mart/sales_over_time.png")
plt.close()

# ---------------------------
# 2. Top Products (Improved)
# ---------------------------
top_products = (
    df.groupby("product_name")["price_egp"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

# shorten long names
top_products.index = top_products.index.str[:20] + "..."

plt.figure(figsize=(10, 6))
ax = top_products.sort_values().plot(kind="barh")

# add values on bars
for i, v in enumerate(top_products.sort_values()):
    ax.text(v, i, f"{int(v):,}", va='center')

plt.title("Top 10 Products")
plt.xlabel("Sales (EGP)")
plt.ylabel("Product")

plt.tight_layout()
plt.savefig("data/mart/top_products.png")
plt.close()

# ---------------------------
# 3. Late Deliveries
# ---------------------------
late_counts = df["late_delivery"].value_counts()

plt.figure(figsize=(6, 4))
ax = late_counts.plot(kind="bar")

# add values on bars
for i, v in enumerate(late_counts):
    ax.text(i, v, str(v), ha='center')

plt.title("Late Deliveries Distribution")
plt.xlabel("Late Delivery")
plt.ylabel("Count")

plt.tight_layout()
plt.savefig("data/mart/late_deliveries.png")
plt.close()

print("📊 Visualizations Created Successfully")