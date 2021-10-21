import boto3
from sagemaker_monitor import Settings
import json


data_capture_prefix = "data_capture_prefix"
endpoint_name = "endpoint_name"
bucket = "bucket_name"

def view_capture_data():
    s3_client = boto3.Session().client("s3")
    current_endpoint_capture_prefix = "{}/{}".format(data_capture_prefix, endpoint_name)
    
    result = s3_client.list_objects(Bucket=bucket, Prefix=current_endpoint_capture_prefix)
    
    capture_files = [capture_file.get("Key") for capture_file in result.get("Contents")]
    
    print("Arquivos Capturados:")
    print("\n ".join(capture_files))
    
    get_obj_body(capture_files[-1])
    
    print("Check Primeiras Linhas")
    print(capture_file[:10])
    
 def get_obj_body(obj_key):
     return s3_client.get_object(Bucket=bucket, Key=obj_key).get("Body").read().decode("urf-8")
    
    #capture_file = get_obj_body(capture_files[-1])
    #print(capture_file[:2000])
