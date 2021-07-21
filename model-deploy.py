#Deps
import os
import boto3
import re
import json
from sagemaker import get_execution_role, session

region = boto3.Session().region_name

role = get_execution_role()

