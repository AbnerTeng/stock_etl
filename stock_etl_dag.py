from datetime import datetime, timedelta

from scripts.fetch_stock_data import fetch_stock_data
from scripts.process_stock_data import process_and_save_stock_data

from airflow.decorators import dag

default_args = {
    "owner": "sinopac",
    "depends_on_past": False,
    "start_date": datetime(2025, 2, 27, 0, 0),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


@dag(
    "weekly_stock_data_fetch",
    default_args=default_args,
    description="A DAG to fetch stock data weekly and save to csv files",
    schedule_interval="@weekly",
    catchup=False,
)
def stock_etl_pipeline():
    stock_data = fetch_stock_data()
    process_and_save_stock_data(stock_data)


etl_dag = stock_etl_pipeline()
