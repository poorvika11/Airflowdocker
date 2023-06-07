from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from sqlalchemy import create_engine

def check_all_dags_run():
    
    engine = create_engine('postgresql://airflow:airflow@localhost:5432/test')

    # Define the time frame for checking DAG execution
    start_time = datetime(2023, 5, 31, 0, 0, 0)  # Specify your desired start time
    end_time = datetime(2023, 6, 1, 0, 0, 0)    # Specify your desired end time

    # Execute the query to check if all DAGs have run within the specified time frame
    with engine.connect() as connection:
        result = connection.execute(f'''
            SELECT COUNT(DISTINCT dag_id) = SUM(CASE WHEN execution_date >= '{start_time}' AND execution_date <= '{end_time}' THEN 1 ELSE 0 END) AS all_dags_run
            FROM dag_runs;
        ''')
        all_dags_run = result.scalar()

    if all_dags_run:
        print("All DAGs have run within the specified time frame.")
    else:
        print("Some DAGs have not run within the specified time frame.")

with DAG(
    'check_all_dags_run',
    start_date=datetime(2023, 6, 1),
    schedule_interval='@daily',
) as dag:
    check_all_dags_operator = PythonOperator(
        task_id='check_all_dags_operator',
        python_callable=check_all_dags_run
    )
