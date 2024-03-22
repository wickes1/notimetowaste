from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator

default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="dag_with_postgres_operator",
    default_args=default_args,
    description="This DAG uses the PostgresOperator",
    start_date=datetime(2024, 3, 1),
    schedule_interval="0 3 * * Tue-Fri",
    catchup=True,
) as dag:
    create_table = PostgresOperator(
        task_id="create_table",
        postgres_conn_id="postgres_default",
        sql="""
        CREATE TABLE IF NOT EXISTS dag_runs(
                dag_id VARCHAR(250) NOT NULL,
                execution_date TIMESTAMP NOT NULL,
                state VARCHAR(50),
                primary key(dag_id, execution_date)
        )
        """,
    )

    insert_data = PostgresOperator(
        task_id="insert_data",
        postgres_conn_id="postgres_default",
        sql="""
        INSERT INTO dag_runs(dag_id, execution_date, state)
        VALUES('{{ dag.dag_id }}', '{{ ts }}', 'success')
        """,
    )

    delete_data = PostgresOperator(
        task_id="delete_data",
        postgres_conn_id="postgres_default",
        sql="""
        DELETE FROM dag_runs
        WHERE execution_date = '{{ ts }}' AND dag_id = '{{ dag.dag_id }}'
        """,
    )

    create_table >> delete_data >> insert_data
