from airflow.operators.python import PythonOperator
from airflow import DAG
import pendulum

import main_pipe.scripts.stt_billing.pipelines as function

default_args = {
    "owner": "farhan.andika",   
    "description": "M+ Software: Data Engineer (Python) - Airflow Assignment",
}

dag = DAG(
    dag_id='billing-pipeline',
    schedule=None,
    start_date=pendulum.now('Asia/Jakarta'),
    default_args=default_args,
    catchup=False,
    params={
        'overrides': ''
    },
    max_active_runs=1
    )

with dag:
    task_1 = PythonOperator(
        task_id='check-filename',
        python_callable=function.check_file,
        op_kwargs="{{ params.overrides }}",
        trigger_rule="all_success"
    )
    
    task_2 = PythonOperator(
        task_id='data-processing',
        python_callable=function.data_processing,
        trigger_rule="all_done"
    )
    
    task_1 >> task_2