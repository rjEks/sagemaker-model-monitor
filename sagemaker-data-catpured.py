import boto3
from sagemaker_monitor import Settings


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