from sqlalchemy import create_engine

engine = create_engine("postgresql://scott:tiger@localhost:5432/mydatabase")
# import the request library
import requests
import os

# provide the location of your airflow instance
ENDPOINT_URL = "http://localhost:8080/"

# in this example env variables were used to store login information
# you will need to provide your own credentials
user_name = os.environ["airflow"]
password = os.environ["airflow"]

# query the API for successful task instances from all dags and all dag runs (~)
req = requests.get(
    f"{ENDPOINT_URL}/api/v1/dags/~/dagRuns/~/taskInstances?state=success",
    auth=(user_name, password),
)

# from the API response print the value for "total entries"
print(req.json()["total_entries"])


