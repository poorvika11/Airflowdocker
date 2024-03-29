
from datetime import datetime
from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python_operator import PythonOperator


def check_dag_run_status():
    postgres_hook = PostgresHook(postgres_conn_id='postgres_localhost')

    query = """
        SELECT dag_id, MAX(end_date) AS last_run_date, COUNT(*) AS run_count
        FROM dag_run
        GROUP BY dag_id;
    """

    results = postgres_hook.get_records(sql=query)

    for result in results:
        dag_id, last_run_date, run_count = result
        if run_count > 0:
            if last_run_date:
                print(f"DAG '{dag_id}' has been run.")
                scheduled = is_scheduled_on_time(dag_id, last_run_date, postgres_hook)
                if scheduled:
                    print(f"DAG '{dag_id}' was run on its scheduled time.")
                    within_execution_time = is_within_execution_time(dag_id, last_run_date, postgres_hook)
                    if within_execution_time:
                        print(f"DAG '{dag_id}' was run within the expected execution time.")
                    else:
                        print(f"DAG '{dag_id}' exceeded the expected execution time.")
                else:
                    print(f"DAG '{dag_id}' was not run on its scheduled time.")
            else:
                print(f"DAG '{dag_id}' has not been run.")
        else:
            print(f"DAG '{dag_id}' has no runs.")


def is_scheduled_on_time(dag_id, last_run_date, postgres_hook):
    query = f"""
        SELECT start_date, dag.schedule_interval
        FROM dag, dag_run
        WHERE dag.dag_id = '{dag_id}'
        AND dag_run.dag_id = dag.dag_id
        AND dag_run.end_date = '{last_run_date}';
    """

    result = postgres_hook.get_first(sql=query)
    if result:
        start_date, schedule_interval = result
        if schedule_interval and start_date == last_run_date:
            return True

    return False


def is_within_execution_time(dag_id, last_run_date, postgres_hook):
    query = f"""
        SELECT execution_date, MAX(end_date) AS max_end_date
        FROM task_instance
        WHERE dag_id = '{dag_id}'
        AND end_date IS NOT NULL
        GROUP BY execution_date;
    """

    results = postgres_hook.get_records(sql=query)
    for result in results:
        execution_date, max_end_date = result
        if max_end_date and max_end_date <= execution_date:
            return False

    return True


default_args = {
    'start_date': datetime(2023, 6, 7),
    'catchup': False
}

with DAG('dag_run_check', default_args=default_args, schedule_interval='0 */6 * * *') as dag:
    check_all_dag_runs = PythonOperator(
        task_id='check_dag_run_status',
        python_callable=check_dag_run_status
    )
