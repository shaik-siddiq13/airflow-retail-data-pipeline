
# Retail ETL Pipeline Using Apache Airflow

## Project Overview

An end-to-end Retail ETL pipeline built using Apache Airflow, Python, Pandas, Docker, and PostgreSQL.

The pipeline extracts retail sales data from CSV files, performs data cleaning and transformation, loads the processed data into a PostgreSQL data warehouse, and supports business analysis through SQL queries.

## Technology Stack

- Python
- Apache Airflow 3.4.0
- Pandas
- PostgreSQL 16
- Docker and Docker Compose
- SQL

## Architecture

```text
Raw Retail CSV
      |
      v
Apache Airflow
      |
      v
Extract Task
      |
      v
Transform Task
(Python + Pandas)
      |
      v
Cleaned Retail CSV
      |
      v
Load Task
      |
      v
PostgreSQL Data Warehouse
      |
      v
SQL Analytics
```

## ETL Workflow

### 1. Extract
- Read raw retail sales data from CSV.
- Capture the source records using Pandas.
- Save the extracted data.

### 2. Transform
- Remove duplicate records.
- Handle missing customer IDs and product names.
- Filter invalid quantities and unit prices.
- Convert order dates into datetime format.
- Calculate revenue after discount.

### 3. Load
- Connect to PostgreSQL using Airflow PostgresHook.
- Load cleaned records into the retail_sales table.
- Use a database transaction for the load operation.

## Project Results

| Metric | Result |
|---|---:|
| Raw records | 10,025 |
| Cleaned records | 9,886 |
| Raw columns | 11 |
| Cleaned columns | 12 |
| Total revenue | INR 502,307,198.80 |

## SQL Analytics

The project includes eight SQL queries:

1. Category-wise revenue analysis
2. Region-wise revenue analysis
3. Monthly revenue analysis
4. Top five products by revenue
5. Payment method analysis
6. Average order value
7. Highest revenue product in each region
8. Highest revenue product in each category

## Project Structure

```text
airflow-retail-data-pipeline/
|
|-- dags/
|   |-- first_retail_dag.py
|   |-- retail_etl_dag.py
|
|-- data/
|   |-- retail_sales_raw.csv
|   |-- retail_sales_extracted.csv
|   |-- retail_sales_cleaned.csv
|
|-- scripts/
|   |-- generate_retail_data.py
|
|-- sql/
|   |-- 01_category_revenue.sql
|   |-- 02_region_revenue.sql
|   |-- 03_monthly_revenue.sql
|   |-- 04_top_products.sql
|   |-- 05_payment_analysis.sql
|   |-- 06_average_order_value.sql
|   |-- 07_top_product_by_region.sql
|   |-- 08_top_product_by_category.sql
|
|-- docs/
|   |-- architecture.md
|   |-- data_quality.md
|
|-- screenshots/
|-- config/
|-- plugins/
|-- logs/
|
|-- docker-compose.yaml
|-- .gitignore
|-- README.md
```

## How to Run

### Prerequisites
- Docker Desktop
- Git
- Python knowledge

### Start the environment

```bash
docker compose up -d
```

### Access Airflow

Open:

http://localhost:8080

Default local development credentials:

- Username: airflow
- Password: airflow

### Run the Pipeline

1. Open the Airflow UI.
2. Find `retail_etl_pipeline`.
3. Trigger the DAG.
4. Monitor the Extract, Transform, and Load tasks.
5. Verify the loaded records in PostgreSQL.

## Database Details

- Database: `retail_warehouse`
- Table: `retail_sales`
- Database engine: PostgreSQL 16

## Documentation

- [Architecture](docs/architecture.md)
- [Data Quality](docs/data_quality.md)

## Key Learning Outcomes

- Building and running Airflow DAGs.
- Understanding task dependencies.
- Implementing Extract, Transform, and Load operations.
- Using Pandas for data processing.
- Integrating Airflow with PostgreSQL.
- Writing SQL queries for business analytics.
- Running data engineering services using Docker Compose.
