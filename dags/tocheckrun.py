from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from sqlalchemy import create_engine

def check_all_dags_run():
    
    engine = create_engine('postgresql://airflow:airflow@localhost:5432/test')

    
    with engine.connect() as connection:
        result = connection.execute('''
            SELECT COUNT(DISTINCT dag_id) = SUM(CASE WHEN run_status = 'completed' THEN 1 ELSE 0 END) AS all_dags_run
            FROM dag_runs;
        ''')
        all_dags_run = result.scalar()

    if all_dags_run:
        print("All DAGs have run.")
    else:
        print("Some DAGs are pending.")

with DAG(
    'check_all_dags_run',
    start_date=datetime(2023, 6, 1),
    schedule_interval='@daily',
) as dag:
    check_all_dags_operator = PythonOperator(
        task_id='check_all_dags_operator',
        python_callable=check_all_dags_run
    )
