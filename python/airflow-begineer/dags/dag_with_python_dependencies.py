from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


def get_sklearn():
    import sklearn

    print(f"sklearn version: {sklearn.__version__}")


def get_matplotlib():
    import matplotlib

    print(f"matplotlib version: {matplotlib.__version__}")

with DAG(
    dag_id="dag_with_python_dependencies",
    default_args=default_args,
    description="This DAG uses Python dependencies",
    start_date=datetime(2024, 3, 1),
    schedule_interval="0 3 * * Tue-Fri",
    catchup=True,
) as dag:
    task1 = PythonOperator(
        task_id="print_sklearn_version",
        python_callable=get_sklearn,
    )

    task2 = PythonOperator(
        task_id="print_matplotlib_version",
        python_callable=get_matplotlib,
    )

    task1 >> task2
