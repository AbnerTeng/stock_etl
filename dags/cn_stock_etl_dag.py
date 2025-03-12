import os
import warnings
from datetime import datetime, timedelta

from scripts.fetch_cn_stock import fetch_cn_stock

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

warnings.filterwarnings("ignore")


default_args = {
    "owner": "sinopac",
    "depends_on_past": False,
    "start_date": datetime(2025, 3, 17, 0, 0),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT_PATH = os.path.join(BASE_DIR, "scripts", "prepare_cn_data.sh")

def get_last_trading_day(execution_date):
    """Returns the last trading day based on the execution date."""
    execution_day = execution_date.weekday()  # Monday = 0, Sunday = 6
    if execution_day == 5:  # Saturday
        return execution_date - timedelta(days=1)  # Use Friday
    elif execution_day == 6:  # Sunday
        return execution_date - timedelta(days=2)  # Use Friday
    elif execution_day == 0:  # Monday
        return execution_date - timedelta(days=3)  # Use Friday
    else:  # Tuesday - Friday
        return execution_date - timedelta(days=1)  # Use the previous day



with DAG(
    "monthly_cn_stock_data_fetch",
    default_args=default_args,
    description="A DAG to fetch cn stock data monthly and save to csv files",
    schedule_interval="@monthly",
    catchup=False,
) as dag:
    get_date_task = PythonOperator(
        task_id="get_last_trading_day",
        python_callable=get_last_trading_day,
        provide_context=True,
        dag=dag,
    )
    prepare_data_task = BashOperator(
        task_id="prepare_data",
        bash_command=f"bash {SCRIPT_PATH} {{{{ ti.xcom_pull(task_ids='get_last_trading_day') }}}}",
        dag=dag,
    )
    fetch_csi300_task = PythonOperator(
        task_id="fetch_csi300_task",
        python_callable=fetch_cn_stock,
        op_args=["csi300"],
        dag=dag,
    )
    fetch_csi500_task = PythonOperator(
        task_id="fetch_csi500_task",
        python_callable=fetch_cn_stock,
        op_args=["csi500"],
        dag=dag,
    )

    get_date_task >> prepare_data_task >> [fetch_csi300_task, fetch_csi500_task]
