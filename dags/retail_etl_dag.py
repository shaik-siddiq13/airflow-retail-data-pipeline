
import pendulum
import shutil
from pathlib import Path

from airflow.sdk import dag, task


@dag(
    dag_id="retail_etl_pipeline",
    schedule="30 11 * * *",
    start_date=pendulum.datetime(
        2026, 11, 17, tz="Asia/Kolkata"
    ),
    catchup=False,
    max_active_runs=1,
    tags=["retail", "etl", "daily"],
)
def retail_etl_pipeline():

    # TASK 1: EXTRACT
    @task
    def extract_retail_data():

        import pandas as pd

        incoming_dir = Path(
            "/opt/airflow/data/incoming"
        )

        # Discover all pending daily CSV files
        source_files = sorted(
            incoming_dir.glob("retail_sales_*.csv")
        )

        if not source_files:
            raise FileNotFoundError(
                "No pending retail CSV files found."
            )

        dataframes = []

        for file_path in source_files:

            df = pd.read_csv(file_path)

            print("Reading file:", file_path.name)
            print("Rows:", len(df))

            dataframes.append(df)

        # Combine pending files into one batch
        combined_df = pd.concat(
            dataframes,
            ignore_index=True
        )

        extracted_file = (
            "/opt/airflow/data/retail_sales_extracted.csv"
        )

        combined_df.to_csv(
            extracted_file,
            index=False
        )

        print("Total source files:", len(source_files))
        print("Total extracted rows:", len(combined_df))

        return {
            "source_files": [
                str(file) for file in source_files
            ],
            "extracted_file": extracted_file,
        }

    # TASK 2: TRANSFORM
    @task
    def transform_retail_data(input_data):

        import pandas as pd

        df = pd.read_csv(
            input_data["extracted_file"]
        )

        print("Before transformation:", len(df))

        # Remove duplicate records
        df = df.drop_duplicates()

        # Remove missing customer IDs and product names
        df = df.dropna(
            subset=["customer_id", "product_name"]
        )

        # Remove invalid quantities and prices
        df = df[
            (df["quantity"] > 0) &
            (df["unit_price"] > 0)
        ]

        # Convert order date
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

        cleaned_file = (
            "/opt/airflow/data/retail_sales_cleaned.csv"
        )

        df.to_csv(
            cleaned_file,
            index=False
        )

        print("Cleaned file saved:", cleaned_file)

        return {
            "source_files": input_data["source_files"],
            "cleaned_file": cleaned_file,
        }

    # TASK 3: LOAD - INCREMENTAL LOADING
    @task
    def load_retail_data(input_data):

        import pandas as pd
        from airflow.providers.postgres.hooks.postgres import (
            PostgresHook
        )

        df = pd.read_csv(
            input_data["cleaned_file"]
        )

        df["order_date"] = pd.to_datetime(
            df["order_date"]
        ).dt.date

        print("Records ready for loading:", len(df))

        postgres_hook = PostgresHook(
            postgres_conn_id="retail_warehouse_conn"
        )

        conn = postgres_hook.get_conn()

        try:
            with conn:
                with conn.cursor() as cursor:

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
                        ON CONFLICT (order_id) DO NOTHING;
                    """

                    cursor.executemany(
                        insert_query,
                        df.itertuples(
                            index=False,
                            name=None
                        )
                    )

                    inserted_records = cursor.rowcount

            print("Incremental loading completed!")
            print("New records inserted:", inserted_records)
            print(
                "Duplicate records skipped:",
                len(df) - inserted_records
            )

        finally:
            conn.close()

    # TASK 4: ARCHIVE SUCCESSFULLY PROCESSED FILES
    @task
    def archive_retail_files(input_data):

        processed_dir = Path(
            "/opt/airflow/data/processed"
        )

        processed_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        for source_file in input_data["source_files"]:

            source_path = Path(source_file)

            destination = (
                processed_dir / source_path.name
            )

            if destination.exists():
                raise FileExistsError(
                    f"Archive file already exists: {destination}"
                )

            shutil.move(
                str(source_path),
                str(destination)
            )

            print("Archived:", source_path.name)

        print("All source files archived successfully.")

    # TASK DEPENDENCIES
    extracted_data = extract_retail_data()

    cleaned_data = transform_retail_data(
        extracted_data
    )

    load_task = load_retail_data(
        cleaned_data
    )

    archive_task = archive_retail_files(
        cleaned_data
    )

    # Archive only after successful loading
    load_task >> archive_task


retail_etl_pipeline()
