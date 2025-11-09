import duckdb
from minio import Minio
from main_pipe.scripts.stt_billing.helper.files import object_storage_retrieve

def init(bucket_creds:dict, lakehouse_creds:dict) -> None:
    duckdb.sql(f'''
    INSTALL httpfs;
    LOAD httpfs;    

    CREATE OR REPLACE SECRET secret (
        TYPE s3,
        URL_STYLE 'path',
        ENDPOINT '{bucket_creds['endpoint']}',
        KEY_ID '{bucket_creds['access_key']}',
        SECRET '{bucket_creds['access_secret']}',
        USE_SSL 'false'
    );
    ''')
    
    duckdb.sql(f'''
    ATTACH 'dbname={lakehouse_creds['dbname']} user={lakehouse_creds['user']} password={lakehouse_creds['password']} host=postgres port=5432' AS refined (TYPE postgres, SCHEMA 'refined');
    ATTACH 'dbname={lakehouse_creds['dbname']} user={lakehouse_creds['user']} password={lakehouse_creds['password']} host=postgres port=5432' AS marts (TYPE postgres, SCHEMA 'marts');   
    ''')
    
def query_retriever(client:Minio, bucket_name:str, queries:dict) -> list[str]:
    '''
    :return: Return a set of query (create, clean, bad, inject)
    :rtype: list[str]
    '''
    query_objects = [object_storage_retrieve(client, bucket_name, path) for path in queries]
    if all(query_objects):
        return query_objects
    return None

def executor(query:str) -> None:
    duckdb.sql(query)