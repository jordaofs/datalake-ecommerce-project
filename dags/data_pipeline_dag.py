from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id='data_pipeline_dag',
    start_date=datetime(2023, 1, 1),
    schedule_interval='@daily',
    catchup=False
) as dag:

    ingest_bronze = BashOperator(
        task_id='ingest_bronze',
        bash_command='spark-submit --master local[*] /opt/airflow/spark_jobs/bronze/ingest_bronze.py'
    )

    create_silver = BashOperator(
        task_id='create_silver',
        bash_command='spark-submit --master local[*] /opt/airflow/spark_jobs/silver/create_silver.py'
    )

    create_gold = BashOperator(
        task_id='create_gold',
        bash_command='spark-submit --master local[*] /opt/airflow/spark_jobs/gold/create_gold.py'
    )

    ingest_bronze >> create_silver >> create_gold