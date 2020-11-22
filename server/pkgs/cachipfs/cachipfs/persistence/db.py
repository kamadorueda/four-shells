# Third party libraries
import boto3
import botocore.config

# Local libraries
from cachipfs import (
    config,
)

# Constants
RESOURCE = boto3.resource(
    aws_access_key_id=config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
    config=botocore.config.Config(
        max_pool_connections=128,
        parameter_validation=False,
    ),
    region_name=config.AWS_REGION,
    service_name='dynamodb',
    verify=False,
)
