from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'depends_on_past': False,
    'email': ['your-email@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


with DAG('dag_migration', default_args=default_args, schedule_interval='@once') as dag:
    start = DummyOperator(task_id='start')

    # Query to fetch all DAG IDs from PostgreSQL
    fetch_dags_query = "SELECT dag_id FROM dag"

    # Execute the fetch_dags_query
    fetch_dags = PostgresOperator(
        task_id='fetch_dags',
        sql=fetch_dags_query,
        postgres_conn_id='postgres_default'
    )

    # Loop through the DAG IDs and trigger each DAG
    migrate_dags = []
    for dag_id in fetch_dags.output:
        migrate_dag_task = PostgresOperator(
            task_id=f'migrate_dag_{dag_id}',
            sql=f'MIGRATE DAG {dag_id}',  
            postgres_conn_id='postgres_default'
        )
        migrate_dags.append(migrate_dag_task)

    end = DummyOperator(task_id='end')

    # Set the task dependencies
    start >> fetch_dags >> migrate_dags >> end
