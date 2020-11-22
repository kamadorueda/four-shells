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
from cachipfs import (
    persistence,
)


async def ensure_account_exists(*, email: str) -> bool:
    balance: int = 1_000_000
    namespaces: List[str] = []

    try:
        success: bool = await persistence.update(
            ConditionExpression=Attr('email').not_exists(),
            ExpressionAttributeNames={
                '#balance': 'balance',
                '#namespaces': 'namespaces',
            },
            ExpressionAttributeValues={
                ':balance': balance,
                ':namespaces': namespaces,
            },
            Key={
                'email': email.lower(),
            },
            table=persistence.TableEnum.accounts,
            UpdateExpression=(
                'SET #balance = :balance, #namespaces = :namespaces'
            ),
        )

    except ClientError as exc:
        # If the account already exists it's not a problem
        if exc.response['Error']['Code'] == 'ConditionalCheckFailedException':
            success = True
        else:
            raise exc

    return success
