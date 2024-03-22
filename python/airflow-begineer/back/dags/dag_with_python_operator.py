from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from airflow import DAG

default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


def greet(ti) -> str:
    first_name = ti.xcom_pull(task_ids="get_name", key="first_name")
    last_name = ti.xcom_pull(task_ids="get_name", key="last_name")
    quote = ti.xcom_pull(task_ids="get_quote", key="quote")
    return f"Hello {first_name} {last_name}! {quote}"


def get_name(ti):
    ti.xcom_push(key="first_name", value="Kamal")
    ti.xcom_push(key="last_name", value="Choudhary")


def get_quote(ti):
    ti.xcom_push(key="quote", value="To be or not to be, that is the question.")


with DAG(
    default_args=default_args,
    dag_id="dag_with_python_operator",
    description="This DAG uses PythonOperator",
    start_date=datetime(2024, 3, 1),
    schedule_interval="@daily",
) as dag:
    task1 = PythonOperator(
        task_id="greeter",
        python_callable=greet,
        op_kwargs={"name": "Kamal"},
    )

    task2 = PythonOperator(
        task_id="get_name",
        python_callable=get_name,
    )

    task3 = PythonOperator(
        task_id="get_quote",
        python_callable=get_quote,
    )

    [task2, task3] >> task1
