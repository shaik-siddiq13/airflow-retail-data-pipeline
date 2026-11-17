# Retail ETL Pipeline Using Apache Airflow

## Project Overview

An end-to-end Retail ETL pipeline built using Apache Airflow 3.4.0, Python, Pandas, Docker, and PostgreSQL 16.

The pipeline processes daily retail sales CSV files, performs data cleaning and transformation, and loads the processed records into a PostgreSQL data warehouse.

Apache Airflow orchestrates the complete workflow through scheduled DAG execution, task dependencies, and monitoring.

The pipeline also supports incremental data loading, duplicate handling, and automatic archiving of successfully processed source files.

## Technology Stack

- Python
- Apache Airflow 3.4.0
- Pandas
- PostgreSQL 16
- Docker and Docker Compose
- SQL

## Architecture

```text
          Daily Retail CSV
                 |
                 v
          data/incoming/
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
          Load Task
                 |
                 v
       PostgreSQL Data Warehouse
                 |
                 v
            SQL Analytics

          After successful load
                 |
                 v
          Archive Task
                 |
                 v
          data/processed/
```

## ETL Workflow

### 1. Extract

- Discover pending retail CSV files from the incoming directory.
- Read and combine available CSV files using Pandas.
- Prepare extracted data for transformation.
- Process all pending files instead of only the latest file.

### 2. Transform

- Remove duplicate records.
- Handle missing customer IDs and product names.
- Filter invalid quantities and unit prices.
- Convert order dates into datetime format.
- Calculate revenue after applying discounts.
- Generate the cleaned retail dataset.

### 3. Load

- Connect to PostgreSQL using Airflow PostgresHook.
- Load cleaned records into the `retail_sales` table.
- Use `ON CONFLICT (order_id) DO NOTHING` to prevent duplicate order IDs.
- Maintain database consistency during the load operation.

### 4. Archive

- Move successfully processed CSV files from `data/incoming/` to `data/processed/`.
- Archive files only after the database load succeeds.
- Keep incoming files available if an earlier ETL task fails.

## Daily Pipeline Scheduling

The DAG is configured to execute automatically every day.

| Configuration | Value |
|---|---|
| DAG ID | `retail_etl_pipeline` |
| Schedule | Daily at 11:30 AM IST |
| Maximum active runs | 1 |
| Catchup | Disabled |
| Input format | CSV |
| File naming convention | `retail_sales_YYYY-MM-DD.csv` |

### Daily Input Process

New retail CSV files should be placed in:

```text
data/incoming/
```

Example:

```text
data/incoming/
    retail_sales_2026-11-17.csv
    retail_sales_2026-11-18.csv
```

The scheduled DAG discovers and processes all pending CSV files.

Successfully processed files are moved to:

```text
data/processed/
```

### Generate Sample Daily Data

A Python script is included to generate sample retail sales data.

Run from the project root:

```powershell
python .\scripts\generate_daily_retail_data.py
```

The script generates a daily CSV file containing 500 sample retail records.

The generated file is saved in `data/incoming/`.

## Project Results

### Initial Dataset

| Metric | Result |
|---|---:|
| Raw records | 10,025 |
| Cleaned records | 9,886 |
| Raw columns | 11 |
| Cleaned columns | 12 |
| Initial dataset revenue | INR 502,307,198.80 |

### Daily Pipeline Validation

The daily pipeline was tested with two daily CSV batches.

| Metric | Result |
|---|---:|
| Daily records per test batch | 500 |
| Daily test batches | 2 |
| Total records in warehouse | 10,886 |
| Unique order IDs | 10,886 |
| Duplicate order IDs | 0 |

All four DAG tasks completed successfully during the successful end-to-end test.

## SQL Analytics

The project includes eight SQL queries for business analysis:

1. Category-wise revenue analysis
2. Region-wise revenue analysis
3. Monthly revenue analysis
4. Top five products by revenue
5. Payment method analysis
6. Average order value
7. Highest revenue product in each region
8. Highest revenue product in each category

SQL scripts are available in the `sql/` directory.

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
|   |-- incoming/
|   |   |-- .gitkeep
|   |-- processed/
|   |   |-- .gitkeep
|   |-- output/
|       |-- .gitkeep
|
|-- scripts/
|   |-- generate_retail_data.py
|   |-- generate_daily_retail_data.py
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
|
|-- docker-compose.yaml
|-- .gitignore
|-- README.md
```

Generated runtime files, Airflow logs, local configuration, and environment secrets are excluded from Git.

## How to Run

### Prerequisites

- Docker Desktop
- Git
- Python
- Basic knowledge of SQL

### 1. Clone the Repository

```bash
git clone https://github.com/shaik-siddiq13/airflow-retail-data-pipeline.git
```

```bash
cd airflow-retail-data-pipeline
```

### 2. Start Docker Services

```bash
docker compose up -d
```

### 3. Access Airflow

Open the Airflow web interface:

http://localhost:8080

Default local development credentials:

- Username: `airflow`
- Password: `airflow`

### 4. Run the Pipeline

1. Open the Airflow UI.
2. Find the `retail_etl_pipeline` DAG.
3. Enable the DAG if it is paused.
4. Trigger the DAG manually for testing, or wait for its scheduled execution.
5. Monitor the Extract, Transform, Load, and Archive tasks.
6. Verify the records in PostgreSQL.

## Database Details

| Configuration | Value |
|---|---|
| Database engine | PostgreSQL 16 |
| Database | `retail_warehouse` |
| Table | `retail_sales` |
| Airflow connection ID | `retail_warehouse_conn` |

### Verify Loaded Records

Run the following command from the project directory:

```powershell
docker compose exec retail-postgres psql -P pager=off -U retail_user -d retail_warehouse -c "SELECT COUNT(*) AS total_records, COUNT(DISTINCT order_id) AS unique_orders FROM retail_sales;"
```

## Team Execution Model

The project supports individual local development environments.

Each teammate can:

- Clone the GitHub repository.
- Configure and run their own Docker Compose environment.
- Place new CSV files in their local incoming directory.
- Execute and monitor their own Airflow DAG.
- Verify processed records in their own PostgreSQL database.

GitHub is used to share project code and updates. Local Airflow runs and database records are not automatically shared between teammates.

## Documentation

- [Architecture](docs/architecture.md)
- [Data Quality](docs/data_quality.md)

## Key Learning Outcomes

- Building and scheduling Apache Airflow DAGs.
- Understanding task dependencies and orchestration.
- Implementing end-to-end ETL workflows.
- Processing CSV datasets using Python and Pandas.
- Integrating Airflow with PostgreSQL using PostgresHook.
- Implementing incremental loading and duplicate handling.
- Managing daily input files and archiving processed data.
- Writing SQL queries for business analytics.
- Running data engineering services using Docker Compose.