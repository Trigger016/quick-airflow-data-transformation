from json import load, dump
from minio import Minio
    
def exists_filename(mode:str, client:Minio, json_filepath:str, bucket_properties:dict) -> list[str] | None:
    with open(json_filepath, 'r') as jsonbuffer:
        jsonfile = load(jsonbuffer)
    
    if mode == 'retrieve':
        return jsonfile['inject']
    
    existing = jsonfile['exists']
    detected_filename = client.list_objects(
        bucket_name=bucket_properties['name'],
        prefix=bucket_properties['csv_prefix']
    )
    working_list = [filename.object_name for filename in detected_filename 
                    if filename.object_name not in existing
                    and filename.object_name.replace(bucket_properties['csv_prefix'], '') != '']
    
    if len(working_list) > 0:
        return working_list
    return None

def update_json(where:str, json_filepath:str, list_addition:list, mode:str=None) -> None:
    if where not in ('exists', 'inject'):
        raise Exception('Wrong Location')
    
    with open(json_filepath, 'r') as read_buffer:
        jsonfile = load(read_buffer)
            
        if mode:
            jsonfile[where] = list_addition
        else:
            jsonfile[where].extend(list_addition)
            
    with open(json_filepath, 'w') as write_buffer:   
        dump(jsonfile, write_buffer, indent=4)
        
def object_storage_retrieve(client:Minio, bucket_name:str, bucket_path:str) -> str:
    response = None
    try:
        response = client.get_object(
            bucket_name=bucket_name,
            object_name=bucket_path,
        )
        return response.read().decode()
    except Exception:
        return None
    finally:
        if response:
            response.close()
            response.release_conn()
        
    