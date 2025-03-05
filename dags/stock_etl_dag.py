import warnings
from datetime import datetime, timedelta

from scripts.process_stock_data import process_and_save_stock_data

from airflow import DAG
from airflow.operators.python import PythonOperator

warnings.simplefilter("ignore", category=FutureWarning)


default_args = {
    "owner": "sinopac",
    "depends_on_past": False,
    "start_date": datetime(2025, 3, 6, 0, 0),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


with DAG(
    "daily_stock_data_fetch",
    default_args=default_args,
    description="A DAG to fetch stock data daily and save to csv files",
    schedule_interval="@daily",
    catchup=False,
) as dag:
    process_task = PythonOperator(
        task_id="process_and_save_stock_data_task",
        python_callable=process_and_save_stock_data,
        dag=dag,
    )
