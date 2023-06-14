import os
import time
from airflow.models import DagBag

MONITORED_DAGS_DIR = '/Applications/airflow_docker/dags'

def load_dags_from_directory():
    dag_bag = DagBag(dag_folder=MONITORED_DAGS_DIR)
    for dag_id in dag_bag.dag_ids:
        # Check if DAG is already loaded
        if not dag_bag.has_dag(dag_id):
            dag_bag.process_file(os.path.join(MONITORED_DAGS_DIR, dag_id + '.py'))

def run_dynamic_dag_loader():
    while True:
        load_dags_from_directory()
        time.sleep(300)  # Wait for 5 minutes before scanning again

if __name__ == '__main__':
    run_dynamic_dag_loader()
