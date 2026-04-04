# Data Model - Star Schema

## Overview
This module builds the Data Warehouse dimensional model (Star Schema).

## ERD Diagram
![Star Schema ERD](erd_star_schema_detailed.html)

## Tables

### Fact Table
**fact_sales** — contains all sales transactions

| Column         | Type  | Description                |
|---------------|------|----------------------------|
| order_id      | FK   | Order identifier           |
| customer_id   | FK   | Customer identifier        |
| product_id    | FK   | Product identifier         |
| store_id      | FK   | Store identifier           |
| date_id       | FK   | Date identifier            |
| quantity      | int  | Quantity sold              |
| list_price    | float| Product price              |
| discount      | float| Discount applied           |
| total_price   | float| Total transaction amount   |

---

### Dimension Tables

| Table         | Description                          |
|--------------|--------------------------------------|
| dim_customer | Stores customer data                 |
| dim_product  | Stores product, brand, and category  |
| dim_store    | Stores store information             |
| dim_date     | Stores date attributes               |