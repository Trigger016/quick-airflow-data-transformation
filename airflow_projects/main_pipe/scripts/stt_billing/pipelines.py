import duckdb
from airflow.exceptions import AirflowSkipException
from main_pipe.scripts.stt_billing.helper.files import exists_filename, update_json
from main_pipe.scripts.stt_billing.helper.conn import minio_interface
from main_pipe.scripts.stt_billing.helper.query_interface import init, query_retriever, destruct
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
    try:
        client = minio_interface(var.MINIO_CREDS)
        filelist = exists_filename('retrieve', client, var.FILENAME_JSON_PATH, var.BUCKET_PROPERTIES)
        
        init(var.MINIO_CREDS, var.LAKEHOUSE_CREDS)


        # CREATE TABLE IF NOT EXISTS
        one_time_qeuries = query_retriever(client, var.SQL_BUCKET_NAME, var.QUERY, 'one_time')
        if not one_time_qeuries:
            update_json('inject', var.FILENAME_JSON_PATH, [], 'replace')
            raise AirflowSkipException
        
        create_query, mart_query = one_time_qeuries
        duckdb.sql(create_query)
        
        for file in filelist:
            try:
                clean_query, bad_query = query_retriever(client, var.SQL_BUCKET_NAME, var.QUERY)
                
                clean_query = clean_query.format(pattern=file)
                bad_query = bad_query.format(pattern=file)

                duckdb.sql(clean_query)
                duckdb.sql(bad_query)

                update_json('exists', var.FILENAME_JSON_PATH, [file])
                print(f'{file} Injected.')
                
            except Exception as refined_err:
                print(refined_err, '|', file)
                
        duckdb.sql(mart_query)
        update_json('inject', var.FILENAME_JSON_PATH, [], 'replace')
    finally:
        destruct()