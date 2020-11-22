# Standard library
from enum import (
    Enum,
)
from typing import (
    Any,
    List,
    NamedTuple,
)

# Third party libraries
from aioextensions import (
    in_thread,
)
import boto3
import botocore.config

# Local libraries
from cachipfs import (
    config,
)

# Constants
RESOURCE: Any = boto3.resource(
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


class Account(NamedTuple):
    id: int  # Hash key
    balance: int
    email: str
    namespaces: List[str]
    tokens: List[str]


class Namespace(NamedTuple):
    id: int  # Hash key
    name: List[str]


class Object(NamedTuple):
    key: List[str]  # Range key
    namespace: int  # Hash key
    value: List[str]


# References:
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Table.delete_item
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Table.get_item
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Table.update_item


async def get(*, table: TableEnum, **kwargs: Any) -> Any:
    table_resource: Any = RESOURCE.Table(table.value)

    response = await in_thread(table_resource.get_item, **kwargs)

    return response


async def update(*, table: TableEnum, **kwargs: Any) -> bool:
    table_resource: Any = RESOURCE.Table(table.value)

    kwargs['ReturnConsumedCapacity'] = 'NONE'
    response = await in_thread(table_resource.update_item, **kwargs)

    return response['ResponseMetadata']['HTTPStatusCode'] == 200


async def delete(*, table: TableEnum, **kwargs: Any) -> bool:
    table_resource: Any = RESOURCE.Table(table.value)

    response = await in_thread(table_resource.delete_item, **kwargs)

    return response['ResponseMetadata']['HTTPStatusCode'] == 200
