from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor

default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="dag_with_minio_s3_v2",
    default_args=default_args,
    description="This DAG uses Minio S3",
    start_date=datetime(2024, 3, 1),
) as dag:
    task1 = S3KeySensor(
        task_id="s3_key_sensor",
        bucket_name="airflow",
        bucket_key="data.csv",
        aws_conn_id="minio_default",
        mode="poke",
        poke_interval=5,
        timeout=30,
    )

    task1
