import random
from datetime import datetime, timedelta

import pandas as pd


# Reproducible dataset
random.seed(42)

# Dataset configuration
TOTAL_RECORDS = 10000

products = [
    ("Laptop", "Electronics", 55000),
    ("Mobile", "Electronics", 25000),
    ("Headphones", "Electronics", 2000),
    ("Keyboard", "Accessories", 1500),
    ("Mouse", "Accessories", 800),
    ("Office Chair", "Furniture", 7500),
    ("Desk", "Furniture", 12000),
    ("Notebook", "Stationery", 100),
    ("Pen", "Stationery", 20),
    ("Water Bottle", "Lifestyle", 500),
]

regions = ["North", "South", "East", "West", "Central"]
payment_methods = ["UPI", "Credit Card", "Debit Card", "Cash", "Net Banking"]

start_date = datetime(2025, 1, 1)

records = []

for i in range(TOTAL_RECORDS):
    product_name, category, unit_price = random.choice(products)

    order_date = start_date + timedelta(
        days=random.randint(0, 364)
    )

    quantity = random.randint(1, 10)
    discount = round(random.uniform(0, 0.25), 2)

    record = {
        "order_id": f"ORD{i + 1:06d}",
        "order_date": order_date.strftime("%Y-%m-%d"),
        "customer_id": f"CUST{random.randint(1, 2000):04d}",
        "product_id": f"PROD{products.index((product_name, category, unit_price)) + 1:03d}",
        "product_name": product_name,
        "category": category,
        "quantity": quantity,
        "unit_price": unit_price,
        "discount": discount,
        "payment_method": random.choice(payment_methods),
        "region": random.choice(regions),
    }

    records.append(record)


# Convert records into a DataFrame
df = pd.DataFrame(records)


# Introduce intentional data-quality issues

# Missing customer IDs
df.loc[random.sample(range(TOTAL_RECORDS), 50), "customer_id"] = None

# Missing product names
df.loc[random.sample(range(TOTAL_RECORDS), 30), "product_name"] = None

# Invalid quantities
df.loc[random.sample(range(TOTAL_RECORDS), 20), "quantity"] = -1

# Invalid prices
df.loc[random.sample(range(TOTAL_RECORDS), 15), "unit_price"] = -100

# Duplicate records
duplicates = df.sample(25, random_state=42)
df = pd.concat([df, duplicates], ignore_index=True)


# Save raw dataset
output_path = "data/retail_sales_raw.csv"
df.to_csv(output_path, index=False)

print("Retail dataset generated successfully!")
print(f"Total records: {len(df)}")
print(f"Columns: {list(df.columns)}")
print(f"Output file: {output_path}")

print("\nFirst 5 records:")
print(df.head())

print("\nMissing values:")
print(df.isnull().sum())
