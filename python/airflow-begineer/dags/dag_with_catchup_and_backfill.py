"""
Backfill:

docker exec -it <container_id> bash
airflow dags backfill -s 2024-03-01 -e 2024-03-10 dag_with_catchup_and_backfill_v2
"""

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="dag_with_catchup_and_backfill_v2",
    default_args=default_args,
    description="This DAG uses catchup and backfill",
    start_date=datetime(2024, 3, 1),
    schedule_interval="@daily",
    catchup=False,
) as dag:
    task1 = BashOperator(
        task_id="print_date",
        bash_command="date",
    )

    task1
