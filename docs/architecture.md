
# Retail ETL Pipeline - Architecture

## 1. Project Overview

This project implements an end-to-end Retail ETL pipeline using Apache Airflow, Python, Pandas, Docker, and PostgreSQL.

The pipeline extracts retail sales data from a CSV file, cleans and transforms the data, and loads the processed records into a PostgreSQL data warehouse.

## 2. Architecture Flow

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
Transform Task (Python + Pandas)
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

## 3. Components

- **Source:** Raw retail sales CSV dataset.
- **Orchestration:** Apache Airflow DAG.
- **Extraction:** Pandas reads the source CSV.
- **Transformation:** Removes duplicates, handles missing values, filters invalid records, converts data types, and calculates revenue.
- **Loading:** Loads cleaned records into PostgreSQL.
- **Analytics:** SQL queries analyze revenue, products, regions, categories, and payment methods.
- **Environment:** Docker Compose.

## 4. Pipeline Tasks

1. Extract - reads raw retail data.
2. Transform - cleans and prepares the data.
3. Load - inserts cleaned records into PostgreSQL.

## 5. Final Results

- Raw records: 10,025
- Cleaned records: 9,886
- Duplicate records removed: 25
- Missing customer IDs handled: 50
- Missing product names handled: 30
- Invalid quantity and price values identified and filtered
- Total revenue: INR 502,307,198.80

## 6. Database Details

- Database: `retail_warehouse`
- Table: `retail_sales`
- Database engine: PostgreSQL 16
