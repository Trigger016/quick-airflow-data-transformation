import os
from dotenv import load_dotenv
load_dotenv('/opt/airflow/projects/main_pipe/scripts/stt_billing/.env')

FILENAME_JSON_PATH= os.getenv('FILENAME_JSON_PATH')

BUCKET_PROPERTIES = {
    'name': os.getenv('CSV_BUCKET_NAME'),
    'csv_prefix': os.getenv('CSV_BUCKET_PATH')
} 

LAKEHOUSE_CREDS= {
    'user': os.getenv('LAKEHOUSE_USER'),
    'password': os.getenv('LAKEHOUSE_PASS'),
    'dbname': os.getenv('LAKEHOUSE_DB'),
}

MINIO_CREDS= {
    'access_key': os.getenv('MINIO_ACCESS_ID'),
    'access_secret': os.getenv('MINIO_ACCESS_SECRET'),
    'endpoint': os.getenv('MINIO_ENDPOINT').replace('http://', ''),
}

SQL_BUCKET_NAME=os.getenv('SQL_BUCKET_NAME')
SQL_PATH=os.getenv('SQL_PATH')
QUERY = {
    'create': os.path.join(SQL_PATH, 'create_receipts.sql'),
    'clean': os.path.join(SQL_PATH, 'refined_receipts.sql'),
    'bad': os.path.join(SQL_PATH, 'bad_receipts.sql'),
    'inject': os.path.join(SQL_PATH, 'inject_receipts.sql')
}
