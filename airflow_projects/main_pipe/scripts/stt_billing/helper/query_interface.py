import duckdb
from minio import Minio
from main_pipe.scripts.stt_billing.helper.files import object_storage_retrieve

def init(bucket_creds:dict, lakehouse_creds:dict) -> None:
    duckdb.sql(f'''
    INSTALL httpfs;
    INSTALL postgres;
    LOAD httpfs;    
    LOAD postgres;

    CREATE OR REPLACE SECRET secret (
        TYPE s3,
        URL_STYLE 'path',
        ENDPOINT '{bucket_creds['endpoint']}',
        KEY_ID '{bucket_creds['access_key']}',
        SECRET '{bucket_creds['access_secret']}',
        USE_SSL 'false'
    );
    
    CREATE OR REPLACE SECRET postgres_secret (
    TYPE postgres,
    HOST postgres,
    PORT 5432,
    USER '{lakehouse_creds['user']}',
    PASSWORD '{lakehouse_creds['password']}'
);
    ''')
    
    duckdb.sql(f'''
    ATTACH 'dbname={lakehouse_creds['dbname']}' AS postgres_db (TYPE postgres, SECRET postgres_secret);
    USE postgres_db;
    ''')
    
def destruct() -> None:
    duckdb.sql(f'''
    USE memory;
    DETACH postgres_db;
    ''')
    
def query_retriever(client:Minio, bucket_name:str, queries:dict, mode:str=None) -> list[str]:
    '''
    :return: Return a set of query (create, clean, bad, inject)
    '''
    query_objects:list = [object_storage_retrieve(client, bucket_name, queries[key]) for key in queries]

    queries = query_objects[1:3]
    if mode:
        queries = query_objects[::len(query_objects)-1]
        
    if all(queries):
        return queries
    return None