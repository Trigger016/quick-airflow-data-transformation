import duckdb
from airflow.exceptions import AirflowSkipException
from main_pipe.scripts.stt_billing.helper.files import exists_filename, update_json
from main_pipe.scripts.stt_billing.helper.conn import minio_interface
from airflow_projects.main_pipe.scripts.stt_billing.helper.query_interface import init, query_retriever
from main_pipe.scripts.stt_billing.shared import variables as var


def check_file(**kwargs):
    if 'overrides' in kwargs and '.csv' in kwargs.get('overrides'):
        # Return list from 'overrides param
        filelist = kwargs.get('overrides').strip().split(',')
    else:
        client = minio_interface(var.MINIO_CREDS)
        # Return list detected with ListObjects from csv landing bucket
        filelist = exists_filename('default', client, var.FILENAME_JSON_PATH, var.BUCKET_PROPERTIES)

    if not filelist:
        raise AirflowSkipException
    
    # Change all the actionable files into injection queue list
    update_json('inject', var.FILENAME_JSON_PATH, filelist)
    
def data_processing():
    client = minio_interface(var.MINIO_CREDS)
    filelist = exists_filename('retrieve', client, var.FILENAME_JSON_PATH, var.BUCKET_PROPERTIES)
    
    init(var.MINIO_CREDS, var.LAKEHOUSE_CREDS)
    
    # CREATE TABLE IF NOT EXISTS
    query_objects = query_retriever(client, var.SQL_BUCKET_NAME, var.QUERY)
    if not query_objects:
        update_json('inject', var.FILENAME_JSON_PATH, [], 'replace')
        raise AirflowSkipException
    
    create_query, clean_query, bad_query, inject_query = query_objects
    duckdb.sql(create_query)
    # duckdb.sql(clean_query)
    # duckdb.sql(bad_query)
    # duckdb.sql(inject_query)
    
    
    
    