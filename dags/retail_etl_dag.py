
from datetime import datetime, timezone

from airflow.sdk import dag, task


@dag(
    dag_id="retail_etl_pipeline",
    schedule=None,
    start_date=datetime(2026, 11, 17, tzinfo=timezone.utc),
    catchup=False,
    tags=["retail", "etl", "learning"],
)
def retail_etl_pipeline():

    # TASK 1: EXTRACT
    @task
    def extract_retail_data():

        import pandas as pd

        input_file = "/opt/airflow/data/retail_sales_raw.csv"

        # Read raw retail data
        df = pd.read_csv(input_file)

        print("Retail data extracted successfully!")
        print("Total rows:", len(df))
        print("Total columns:", len(df.columns))

        # Save extracted data
        output_file = "/opt/airflow/data/retail_sales_extracted.csv"

        df.to_csv(output_file, index=False)

        print("Extracted file saved:", output_file)

        return output_file

    # TASK 2: TRANSFORM
    @task
    def transform_retail_data(input_file):

        import pandas as pd

        # Read extracted data
        df = pd.read_csv(input_file)

        print("Before transformation:", len(df))

        # Remove duplicate records
        df = df.drop_duplicates()

        # Remove rows with missing customer ID or product name
        df = df.dropna(
            subset=["customer_id", "product_name"]
        )

        # Remove invalid quantities and prices
        df = df[
            (df["quantity"] > 0) &
            (df["unit_price"] > 0)
        ]

        # Convert order_date to datetime
        df["order_date"] = pd.to_datetime(
            df["order_date"]
        )

        # Calculate revenue after discount
        df["revenue"] = (
            df["quantity"] *
            df["unit_price"] *
            (1 - df["discount"])
        ).round(2)

        print("After transformation:", len(df))
        print("Total revenue:", df["revenue"].sum())

        # Save cleaned data
        output_file = "/opt/airflow/data/retail_sales_cleaned.csv"

        df.to_csv(output_file, index=False)

        print("Cleaned file saved:", output_file)

        return output_file

    # TASK 3: LOAD
    @task
    def load_retail_data(input_file):

        import pandas as pd
        from airflow.providers.postgres.hooks.postgres import PostgresHook

        # Read cleaned CSV
        df = pd.read_csv(input_file)

        # Convert order_date to Python date
        df["order_date"] = pd.to_datetime(
            df["order_date"]
        ).dt.date

        print("Records ready for loading:", len(df))

        # Connect to PostgreSQL using Airflow connection
        postgres_hook = PostgresHook(
            postgres_conn_id="retail_warehouse_conn"
        )

        conn = postgres_hook.get_conn()

        try:
            with conn:
                with conn.cursor() as cursor:

                    # Remove previous records before reloading
                    cursor.execute(
                        "TRUNCATE TABLE retail_sales"
                    )

                    # Insert cleaned records
                    insert_query = """
                        INSERT INTO retail_sales (
                            order_id,
                            order_date,
                            customer_id,
                            product_id,
                            product_name,
                            category,
                            quantity,
                            unit_price,
                            discount,
                            payment_method,
                            region,
                            revenue
                        )
                        VALUES (
                            %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s, %s
                        )
                    """

                    cursor.executemany(
                        insert_query,
                        df.itertuples(
                            index=False,
                            name=None
                        )
                    )

            print("Data loaded successfully into PostgreSQL!")
            print("Total records loaded:", len(df))

        finally:
            conn.close()

    # TASK DEPENDENCIES
    extracted_file = extract_retail_data()

    cleaned_file = transform_retail_data(extracted_file)

    load_retail_data(cleaned_file)


retail_etl_pipeline()
