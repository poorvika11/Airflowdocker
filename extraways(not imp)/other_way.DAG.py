from airflow.models.dagbag import DagBag

from airflow.models.dagrun import DagRun

dag = DagBag().get_dag(src_dag_name)

last_dagrun_run_id = dag.get_last_dagrun(include_externally_triggered=True)

dag_runs = DagRun.find(dag_id=src_dag_name)
for dag_run in dag_runs:
    # get the dag_run details for the Dag that triggered this
    if dag_run.execution_date == last_dagrun_run_id.execution_date:
        print("EXECUTED")