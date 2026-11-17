from datetime import datetime, timezone

from airflow.sdk import dag, task


@dag(
    dag_id="first_retail_dag",
    schedule=None,
    start_date=datetime(2026, 11, 17, tzinfo=timezone.utc),
    catchup=False,
    tags=["learning", "retail"],
)
def first_retail_dag():

    @task
    def say_hello():
        print("Hello! My first Airflow DAG is running.")
        print("Next, we will build a Retail ETL Pipeline.")

    say_hello()


first_retail_dag()
