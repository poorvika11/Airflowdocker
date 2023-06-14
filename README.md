## DAG Run Check in Airflow
This project provides a query-based DAG (Directed Acyclic Graph) for checking the run status of all DAGs in Airflow's metadata. The DAG connects to the Airflow metadata database and retrieves information about the last run date and run count for each DAG. It then checks if the DAG has been run, whether it was run on its scheduled time, and if it was executed within the expected execution time.

## Features
- Retrieves the run status of all DAGs in Airflow's metadata
- Checks if a DAG has been run or not
- Verifies if a DAG was run on its scheduled time
- Validates if a DAG was executed within the expected execution time

## Usage
- Ensure you have Airflow installed and configured properly with database connectivity.
- Place the provided DAG file in your Airflow DAGs directory.
- Update the `db_connect.py` file with your Airflow metadata database connection details.
   - `engine = create_engine("db_connection_url")`
   - `ENDPOINT_URL = "provide the location of your airflow instance"`
- Customize the `to_check_run.py` as needed (e.g., adjust the start date).
- Start the Airflow scheduler to automatically run the DAG according to the specified schedule.

## Configuration
**PostgreSQL Connection** : The DAG requires a PostgreSQL connection configured in your Airflow instance. Make sure to update the postgres_conn_id in the `to_check_run.py` file with the appropriate connection ID `postgres_hook = PostgresHook(postgres_conn_id='*connection_id*')` for your Airflow metadata database.
