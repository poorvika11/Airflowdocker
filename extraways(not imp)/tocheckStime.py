from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from sqlalchemy import create_engine

def check_all_dags_run():
    
    engine = create_engine('postgresql://airflow:airflow@localhost:5432/test')

    
    current_time = datetime.now()
    previous_execution_time = current_time - timedelta(days=1)

    
    with engine.connect() as connection:
        result = connection.execute(f'''
            SELECT COUNT(DISTINCT dag_id) = SUM(CASE WHEN execution_date >= '{previous_execution_time}' THEN 1 ELSE 0 END) AS all_dags_run
            FROM dag_runs;
        ''')
        all_dags_run = result.scalar()

    if all_dags_run:
        print("All DAGs have run at their scheduled time.")
    else:
        print("Some DAGs have not run at their scheduled time.")

with DAG(
    'check_all_dags_run',
    start_date=datetime(2023, 6, 1),
    schedule_interval='@daily',
) as dag:
    check_all_dags_operator = PythonOperator(
        task_id='check_all_dags_operator',
        python_callable=check_all_dags_run
    )
