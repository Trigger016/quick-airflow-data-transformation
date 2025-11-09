from airflow.operators.python import PythonOperator
from airflow import DAG
import pendulum

# from main_pipe.scripts.billing_pipeline


# from airflow.decorators import dag, task
default_args = {
    "owner": "farhan.andika",   
    "description": "M+ Software: Data Engineer (Python) - Airflow Assignment",
}

dag = DAG(
    dag_id='billing-pipeline',
    schedule=None,
    start_date=pendulum.now('Asia/Jakarta'),
    default_args=default_args,
    catchup=False
    )

    