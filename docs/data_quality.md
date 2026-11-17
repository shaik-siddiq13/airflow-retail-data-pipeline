# Retail ETL Pipeline - Data Quality

## 1. Source Dataset

- File: retail_sales_raw.csv
- Initial records: 10,025
- Columns: 11

## 2. Data Quality Issues

The source dataset contains intentionally introduced data quality issues:

- Duplicate records
- Missing customer IDs
- Missing product names
- Invalid quantities
- Invalid unit prices

## 3. Transformation Rules

The Airflow transformation task applies these rules:

1. Remove duplicate records.
2. Remove rows with missing customer IDs.
3. Remove rows with missing product names.
4. Filter records with quantity less than or equal to zero.
5. Filter records with unit price less than or equal to zero.
6. Convert order_date into datetime format.
7. Calculate revenue after discount.

Revenue formula:

revenue = quantity * unit_price * (1 - discount)

## 4. Validation Results

| Validation | Result |
|---|---:|
| Raw records | 10,025 |
| Cleaned records | 9,886 |
| Duplicate records remaining | 0 |
| Missing customer IDs remaining | 0 |
| Missing product names remaining | 0 |
| Invalid quantities remaining | 0 |
| Invalid prices remaining | 0 |

## 5. Final Outcome

The transformation process produced 9,886 cleaned records, ready for loading into the PostgreSQL data warehouse.