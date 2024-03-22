from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="our_first_dag_v2",
    description="This is our first DAG",
    default_args=default_args,
    start_date=datetime(2024, 3, 1),
    schedule_interval="@daily",
) as dag:
    task1 = BashOperator(
        task_id="first_task", bash_command='echo "Hello World! This is the first task."'
    )

    task2 = BashOperator(
        task_id="second_task", bash_command="echo 'This is the second task'"
    )

    task3 = BashOperator(
        task_id="third_task", bash_command="echo 'This is the third task'"
    )

    # task1.set_downstream(task2)
    # task1.set_downstream(task3)

    # task1 >> task2
    # task1 >> task3

    task1 >> [task2, task3]
