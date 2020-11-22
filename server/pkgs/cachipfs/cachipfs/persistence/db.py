# Standard library
from enum import (
    Enum,
)
from typing import (
    Any,
)

# Third party libraries
from aioextensions import (
    in_thread,
)
import boto3
from boto3.resources.factory.dynamodb import (
    ServiceResource as ServiceResourceType,
    Table as TableType,
)
import botocore.config

# Local libraries
from cachipfs import (
    config,
)

# Constants
RESOURCE: ServiceResourceType = boto3.resource(
    aws_access_key_id=config.AWS_ACCESS_KEY_ID_SERVER,
    aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY_SERVER,
    config=botocore.config.Config(
        max_pool_connections=128,
        parameter_validation=False,
    ),
    region_name=config.AWS_REGION,
    service_name='dynamodb',
    verify=False,
)


class TableEnum(Enum):
    accounts: str = 'cachipfs_accounts'
    namespaces: str = 'cachipfs_namespaces'
    objects: str = 'cachipfs_objects'


# References:
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Table.get_item
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Table.put_item
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Table.delete_item


async def get(table: TableEnum, *args: Any, **kwargs: Any) -> Any:
    table_resource: TableType = RESOURCE.Table(table.value)

    response = await in_thread(table_resource.get_item, *args, **kwargs)

    return response


async def put(table: TableEnum, *args: Any, **kwargs: Any) -> Any:
    table_resource: TableType = RESOURCE.Table(table.value)

    response = await in_thread(table_resource.put_item, *args, **kwargs)

    return response


async def delete(table: TableEnum, *args: Any, **kwargs: Any) -> Any:
    table_resource: TableType = RESOURCE.Table(table.value)

    response = await in_thread(table_resource.delete_item, *args, **kwargs)

    return response
