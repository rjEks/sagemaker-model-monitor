#Dependencias
import boto3
import os
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
        self._bucket = bucket
        self._prefix = prefix
        self._data_capture_prefix = data_catpure_prefix
        self._s3_capture_upload_path = "s3://{}/{}".format(self.bucket, self._data_capture_prefix)
        self._reports_prefix = "{}/reports".format(self._prefix)
        self._s3_report_path = "s3://{}/{}".format(self._bucket, self._reports_prefix)
        self._code_prefix = "{}/code".format(self._prefix)
        self._code_preprocessor = "s3://{}/{}/{}".format(bucket, self._code_prefix, code_preprocessor)
        self._code_postprocessor = "s3://{}/{}/{}".format(bucket, self._code_prefix, code_postprocessor)
        self._region = boto3.Session().region_name
        self._role = get_execution_role()

    def upload_model(self):
        """
        Upload do Sagemaker Model XGBoost( pré treinado ) para o bucket S3
        """
        try:
            model_file = open("model/xgb-churn-prediction-model.tar.gz", "rb")
            s3_key = os.path.join(self.prefix, "xgb-churn-prediction-model.tar.gz")
            boto3.Session().resource("s3").Bucket(self._bucket).Object(s3_key).upload_fileobj(model_file)
        except Exception as e:
            print(e)

    def deploy_sagemaker_endpoint(self):
        """
        Deploy de um Sagemaker endpoint utilizando um Sagemaker model como base
        """
        try:
            from time import gmtime, strftime
            from sagemaker.model import Model
            from sagemaker.image_uris import retrieve
            from sagemaker.model_monitor import DataCaptureConfig

            model_name = "sagemaker-model-monitor-xgboost" + strftime("%Y-%m-%d\-%H-%M-%S", gmtime())
            model_url = "https://{}.s3-{}.amazonaws.com/{}/xgb-churn-prediction-model.tar.gz".format(
            self._bucket, self._region, self._prefix)

            image_uri = retrieve("xgboost", self._region, "0.90-1")
            model = Model(image_uri=image_uri, model_data=model_url, role=self._role)
            
            endpoint_name= "sagemaker-endpoint-xgboost-churn-" + strftime("%Y-%m-%d-%H-%M-%S", gmtime())
            data_capture_config = DataCaptureConfig(enable_capture=True, sampling_percentage=100, destination_s3_uri=self._s3_capture_upload_path)

            endpoint = model.deploy(
                initial_instance_count=1,
                instance_type="ml.m4.xlarge",
                endpoint_name=endpoint_name,
                data_capture_config=data_capture_config,
            )

            return endpoint
            
        except Exception as e:
            print(e)

    def invoke_sagemaker_endpoint(endpoint):
        from sagemaker.predictor import Predictor
        from sagemaker.serializers import CSVSerializer
        import time
        
        #Geracao dos arquivos de teste
        
        #Predictor
        predictor = Predictor(endpoint_name=endpoint.endpoint_name, serializer=CSVSerializer())
        
    
    
    
    @property
    def bucket(self):
        return self._bucket




