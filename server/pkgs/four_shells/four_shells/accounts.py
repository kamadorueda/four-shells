# Standard library
from typing import (
    List,
)

# Third party libraries
from botocore.exceptions import (
    ClientError,
)
from boto3.dynamodb.conditions import (
    Attr,
)

# Local libraries
from four_shells import (
    persistence,
)


async def ensure_account_exists(*, email: str) -> bool:
    balance: int = 1_000_000
    cachipfs_namespaces: List[str] = []

    try:
        success: bool = await persistence.update(
            ConditionExpression=Attr('email').not_exists(),
            ExpressionAttributeNames={
                '#balance': 'balance',
                '#cachipfs_namespaces': 'cachipfs_namespaces',
            },
            ExpressionAttributeValues={
                ':balance': balance,
                ':cachipfs_namespaces': cachipfs_namespaces,
            },
            Key={
                'email': email.lower(),
            },
            table=persistence.TableEnum.accounts,
            UpdateExpression=(
                'SET #balance = :balance,'
                '    #cachipfs_namespaces = :cachipfs_namespaces'
            ),
        )

    except ClientError as exc:
        # If the account already exists it's not a problem
        if exc.response['Error']['Code'] == 'ConditionalCheckFailedException':
            success = True
        else:
            raise exc

    return success
