from datetime import datetime, timedelta

from airflow.decorators import dag, task

default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


@dag(
    dag_id="dag_with_taskflow_api",
    default_args=default_args,
    description="This DAG uses TaskFlow API",
    schedule_interval="@daily",
    start_date=datetime(2024, 3, 1),
)
def hello_world_dag():

    @task
    def greet(first_name, last_name, quote) -> str:
        return f"Hello {first_name} {last_name}, {quote}"

    @task(multiple_outputs=True)
    def get_name() -> str:
        return {"first_name": "John", "last_name": "Doe"}

    @task
    def get_quote() -> str:
        return "To be or not to be, that is the question."

    name = get_name()
    quote = get_quote()
    greet(first_name=name["first_name"], last_name=name["last_name"], quote=quote)


greet_dag = hello_world_dag()
