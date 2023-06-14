## DAG Run Check in Airflow
This project provides a query-based DAG (Directed Acyclic Graph) for checking the run status of all DAGs in Airflow's metadata. The DAG connects to the Airflow metadata database and retrieves information about the last run date and run count for each DAG. It then checks if the DAG has been run, whether it was run on its scheduled time, and if it was executed within the expected execution time.

## Features
- Retrieves the run status of all DAGs in Airflow's metadata
- Checks if a DAG has been run or not
- Verifies if a DAG was run on its scheduled time
- Validates if a DAG was executed within the expected execution time
