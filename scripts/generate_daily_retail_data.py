
import pandas as pd
import random
from datetime import date, timedelta
from pathlib import Path


def generate_daily_retail_data():
    batch_date = date.today()
    random.seed()

    output_dir = Path("data/incoming")
    output_dir.mkdir(parents=True, exist_ok=True)

    records = []

    products = {
        "Laptop": ("Electronics", 45000, 85000),
        "Mobile": ("Electronics", 12000, 45000),
        "Headphones": ("Accessories", 500, 5000),
        "Keyboard": ("Accessories", 500, 3000),
        "Mouse": ("Accessories", 300, 2000),
        "Office Chair": ("Furniture", 3000, 12000),
        "Desk": ("Furniture", 4000, 15000),
        "Notebook": ("Stationery", 30, 150),
        "Pen": ("Stationery", 10, 100),
        "Water Bottle": ("Lifestyle", 100, 800),
    }

    payment_methods = [
        "Cash", "UPI", "Debit Card",
        "Credit Card", "Net Banking"
    ]

    regions = ["North", "South", "East", "West", "Central"]

    for i in range(1, 501):
        product_name = random.choice(list(products.keys()))
        category, min_price, max_price = products[product_name]

        order_date = batch_date - timedelta(
            days=random.randint(0, 30)
        )

        records.append({
            "order_id": f"ORD{batch_date:%Y%m%d}{i:06d}",
            "order_date": order_date,
            "customer_id": f"CUST{random.randint(1, 1000):05d}",
            "product_id": f"PROD{list(products).index(product_name)+1:03d}",
            "product_name": product_name,
            "category": category,
            "quantity": random.randint(1, 5),
            "unit_price": round(random.uniform(min_price, max_price), 2),
            "discount": round(random.choice([0, 0.05, 0.10, 0.15]), 2),
            "payment_method": random.choice(payment_methods),
            "region": random.choice(regions),
        })

    df = pd.DataFrame(records)

    file_path = output_dir / (
        f"retail_sales_{batch_date:%Y-%m-%d}.csv"
    )

    if file_path.exists():
        raise FileExistsError(
            f"Today's file already exists: {file_path}"
        )

    df.to_csv(file_path, index=False)

    print("Daily retail CSV generated successfully")
    print("File:", file_path)
    print("Total records:", len(df))
    print("Unique order IDs:", df["order_id"].nunique())


if __name__ == "__main__":
    generate_daily_retail_data()
