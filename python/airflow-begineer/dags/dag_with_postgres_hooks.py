import logging
from datetime import datetime, timedelta

import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from tempfile import NamedTemporaryFile

default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


def postgres_to_s3(ds, next_ds):

    hook = PostgresHook(postgres_conn_id="postgres_default")
    connection = hook.get_conn()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM orders WHERE order_date >= '%s' AND order_date < '%s';"
        % (ds, next_ds)
    )
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    df = pd.DataFrame(results, columns=[col.name for col in cursor.description])

    with NamedTemporaryFile("w", suffix=f"{ds}") as f:
        df.to_csv(f.name, index=False)
        f.flush()

        logging.info("orders_%s.csv created", ds)

        s3_hook = S3Hook(aws_conn_id="minio_default")
        s3_hook.load_file(
            filename=f.name, key=f"orders_{ds}.csv", bucket_name="airflow"
        )

        logging.info("orders_%s.csv uploaded to S3", f.name)


with DAG(
    dag_id="dag_with_postgres_hooks_v4",
    default_args=default_args,
    description="This DAG uses Postgres hooks",
    start_date=datetime(2024, 3, 1),
    schedule_interval="@daily",
    catchup=True,
) as dag:
    task1 = PythonOperator(
        task_id="postgres_to_s3",
        python_callable=postgres_to_s3,
    )
