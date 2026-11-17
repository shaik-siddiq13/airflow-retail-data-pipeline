# Team Setup Guide – Retail ETL Pipeline

## 1. Project Overview

This guide explains how each teammate can configure and run the Retail ETL Pipeline independently on their local machine.

Each teammate will have their own:
- Airflow environment
- PostgreSQL database
- Docker containers
- Local input and processed CSV files

The GitHub repository shares the project code. Airflow execution history and database records remain local to each environment.

## 2. Prerequisites

Install the following tools:

- Git
- Docker Desktop
- Python 3
- Visual Studio Code (recommended)

Ensure Docker Desktop is running before starting the project.

## 3. Clone the Repository

Open PowerShell and run:

```powershell
git clone https://github.com/shaik-siddiq13/airflow-retail-data-pipeline.git
cd airflow-retail-data-pipeline
```

## 4. Configure Environment Variables

The repository includes an `.env.example` file containing the required environment variable names.

Create your own local `.env` file:

```powershell
Copy-Item .env.example .env
```

Open the file:

```powershell
code .env
```

Update the following values with your own credentials:

- `FERNET_KEY`
- `AIRFLOW_POSTGRES_PASSWORD`
- `RETAIL_POSTGRES_PASSWORD`
- `AIRFLOW_JWT_SECRET`
- `_AIRFLOW_WWW_USER_PASSWORD`

Do not use another teammate's secrets.

Keep `.env` private. Never commit it to GitHub.

## 5. Generate Secure Secrets

Each teammate must generate their own secrets.

Run the following command in PowerShell from the project directory:

```powershell
python -c "import secrets,base64; print('FERNET_KEY='+base64.urlsafe_b64encode(secrets.token_bytes(32)).decode()); print('AIRFLOW_JWT_SECRET='+secrets.token_hex(32)); print('AIRFLOW_POSTGRES_PASSWORD='+secrets.token_urlsafe(24)); print('RETAIL_POSTGRES_PASSWORD='+secrets.token_urlsafe(24)); print('_AIRFLOW_WWW_USER_PASSWORD='+secrets.token_urlsafe(24))"
```

The command generates five unique values:

- Fernet encryption key
- Airflow JWT secret
- Airflow metadata database password
- Retail warehouse database password
- Airflow web login password

Copy each generated value into the matching variable in your local `.env` file.

Do not share these secrets or commit them to GitHub.

## 6. Start Docker Services

Make sure Docker Desktop is running.

From the project root directory, execute:

```powershell
docker compose up -d
```

Check the running containers:

```powershell
docker compose ps
```

Wait until the required services are healthy.

## 7. Access Apache Airflow

Open the Airflow web interface:

http://localhost:8080

Log in using the credentials configured in your `.env` file:

- Username: Value of `_AIRFLOW_WWW_USER_USERNAME` (default: `airflow`)
- Password: Value of `_AIRFLOW_WWW_USER_PASSWORD`

## 8. Configure the PostgreSQL Connection

Each teammate must configure the Airflow connection in their own Airflow environment.

Open the Airflow UI:

http://localhost:8080

Navigate to the Connections section and add a new connection with these details:

| Field | Value |
|---|---|
| Connection ID | `retail_warehouse_conn` |
| Connection Type | PostgreSQL |
| Host | `retail-postgres` |
| Database | `retail_warehouse` |
| Username | `retail_user` |
| Password | Your `RETAIL_POSTGRES_PASSWORD` from `.env` |
| Port | `5432` |

Save the connection.

This connection allows Airflow's PostgresHook to communicate with the retail warehouse container.

## 9. Generate Daily Retail Data

From the project root, run:

```powershell
python .\scripts\generate_daily_retail_data.py
```

The script generates 500 sample retail records and saves the CSV file in:

```text
data/incoming/
```

Expected filename format:

```text
retail_sales_YYYY-MM-DD.csv
```

## 10. Execute the ETL Pipeline

The DAG is configured to run daily at 11:30 AM IST.

For manual testing:

1. Open the Airflow UI.
2. Find `retail_etl_pipeline`.
3. Enable the DAG if paused.
4. Trigger the DAG.
5. Monitor all four tasks:
   - `extract_retail_data`
   - `transform_retail_data`
   - `load_retail_data`
   - `archive_retail_files`

After successful execution, processed CSV files are moved to `data/processed/`.

## 11. Verify PostgreSQL Records

Run this command from PowerShell:

```powershell
docker compose exec retail-postgres psql -P pager=off -U retail_user -d retail_warehouse -c "SELECT COUNT(*) AS total_records, COUNT(DISTINCT order_id) AS unique_orders FROM retail_sales;"
```

The query displays the total number of records and unique order IDs in the warehouse.

## 12. Stop Docker Services

To stop the project containers:

```powershell
docker compose down
```

This command preserves the named database volumes.

Do not use `docker compose down -v` unless you intentionally want to delete the database volumes and their stored data.

