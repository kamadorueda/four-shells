# Standard library
from enum import (
    Enum,
)
from typing import (
    Any,
    List,
    Tuple,
)

# Third party libraries
from aioextensions import (
    in_thread,
)
import boto3
import botocore.config

# Local libraries
import config.server

# Constants
RESOURCE: Any = boto3.resource(
    aws_access_key_id=config.server.AWS_ACCESS_KEY_ID_SERVER,
    aws_secret_access_key=config.server.AWS_SECRET_ACCESS_KEY_SERVER,
    config=botocore.config.Config(
        max_pool_connections=128,
        parameter_validation=False,
    ),
    region_name=config.server.AWS_REGION,
    service_name='dynamodb',
    verify=False,
)


class TableEnum(Enum):
    accounts: str = 'accounts'
    cachipfs_namespaces: str = 'cachipfs_namespaces'


# References:
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Table.delete_item
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Table.get_item
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Table.update_item


async def get(*, table: TableEnum, **kwargs: Any) -> Any:
    table_resource: Any = RESOURCE.Table(table.value)

    kwargs['ReturnConsumedCapacity'] = 'NONE'
    response = await in_thread(table_resource.get_item, **kwargs)

    return response['Item']


async def query(*, table: TableEnum, **kwargs: Any) -> Tuple[Any, ...]:
    table_resource: Any = RESOURCE.Table(table.value)

    kwargs['ReturnConsumedCapacity'] = 'NONE'
    response = await in_thread(table_resource.query, **kwargs)
    result: List[Any] = response['Items']

    while 'LastEvaluatedKey' in response:
        kwargs['ExclusiveStartKey'] = response['LastEvaluatedKey']
        response = await in_thread(table_resource.query, **kwargs)
        result.extend(response['Items'])

    return tuple(result)


async def update(*, table: TableEnum, **kwargs: Any) -> bool:
    table_resource: Any = RESOURCE.Table(table.value)

    kwargs['ReturnConsumedCapacity'] = 'NONE'
    response = await in_thread(table_resource.update_item, **kwargs)

    return response['ResponseMetadata']['HTTPStatusCode'] == 200


async def delete(*, table: TableEnum, **kwargs: Any) -> bool:
    table_resource: Any = RESOURCE.Table(table.value)

    kwargs['ReturnConsumedCapacity'] = 'NONE'
    response = await in_thread(table_resource.delete_item, **kwargs)

    return response['ResponseMetadata']['HTTPStatusCode'] == 200
