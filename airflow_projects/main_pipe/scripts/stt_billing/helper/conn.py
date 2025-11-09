from minio import Minio

def minio_interface(creds:dict) -> Minio:
    client = Minio(
        endpoint=creds['endpoint'],
        access_key=creds['access_key'],
        secret_key=creds['access_secret'],
        secure=False
    )
    return client