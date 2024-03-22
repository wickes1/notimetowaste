from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="dag_with_cron_expression",
    default_args=default_args,
    description="This DAG uses cron expression",
    start_date=datetime(2024, 3, 1),
    schedule_interval="0 3 * * Tue-Fri",
    catchup=True,
) as dag:
    task1 = BashOperator(
        task_id="print_date",
        bash_command="date",
    )

    task1
