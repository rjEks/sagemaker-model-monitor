#Dependencias
import boto3
import re
import json
from sagemaker import get_execution_role, session

#Regiao
#boto3.Session().region_name

#role
#role = get_execution_role

class Settings:

    def __init__(self, bucket, prefix, data_catpure_prefix, code_preprocessor, code_postprocessor):
        """
        Configurações iniciais dos buckets, prefixose e scripts que serão utilizados no decorrer da implementação.
        """
        self.bucket = bucket
        self.prefix = prefix
        self.data_capture_prefix = data_catpure_prefix
        self.s3_capture_upload_path = "s3://{}/{}".format(bucket, data_capture_prefix)
        self.reports_prefix = "{}/reports".format(prefix)
        self.s3_report_path = "s3://{}/{}".format(bucket, reports_prefix)
        self.code_prefix = "{}/code".format(prefix)
        self.code_preprocessor = "s3://{}/{}/{}".format(bucket, code_prefix, code_preprocessor)
        self.code_postprocessor = "s3://{}/{}/{}".format(bucket, code_prefix, code_postprocessor)
        self.region = boto3.Session().region_name
        self.role = get_execution_role()

    def upload_model():
        """
        Upload do Sagemaker Model XGBoost( pré treinado ) para o bucket S3
        """
        model_file = open("model/xgb-churn-prediction-model.tar.gz", "rb")
        s3_key = os.path.join(prefix, "xgb-churn-prediction-model.tar.gz")
        boto3.Session().resource("s3").Bucket(bucket).Object(s3_key).upload_fileobj(model_file)

    def deploy_sagemaker_endpoint():
        """
        Deploy de um Sagemaker endpoint utilizando um Sagemaker model como base
        """

