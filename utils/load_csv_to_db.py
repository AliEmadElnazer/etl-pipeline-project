import pandas as pd
import sqlite3


def load_csv_to_db():
    conn = sqlite3.connect("data/orders.db")

    orders = pd.read_csv("data/source/orders.csv")
    order_items = pd.read_csv("data/source/order_items.csv")

    orders.to_sql("orders", conn, if_exists="replace", index=False)
    order_items.to_sql("order_items", conn, if_exists="replace", index=False)

    conn.close()

    print("CSV Loaded to Database ✅")