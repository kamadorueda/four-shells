# Third party libraries
from botocore.exceptions import (
    ClientError,
)
from boto3.dynamodb.conditions import (
    Attr,
)

# Local libraries
from security import (
    create_secret,
)
from server import (
    persistence,
)


async def ensure_account_exists(*, email: str) -> bool:
    cachipfs_api_token: int = create_secret()
    cachipfs_encryption_key: int = create_secret()

    try:
        success: bool = await persistence.update(
            ConditionExpression=Attr('email').not_exists(),
            ExpressionAttributeNames={
                '#cachipfs_api_token': 'cachipfs_api_token',
                '#cachipfs_encryption_key': 'cachipfs_encryption_key',
            },
            ExpressionAttributeValues={
                ':cachipfs_api_token': cachipfs_api_token,
                ':cachipfs_encryption_key': cachipfs_encryption_key,
            },
            Key={
                'email': email,
            },
            table=persistence.TableEnum.accounts,
            UpdateExpression=(
                'SET #cachipfs_api_token = :cachipfs_api_token,'
                '    #cachipfs_encryption_key = :cachipfs_encryption_key,'
            ),
        )

    except ClientError as exc:
        # If the account already exists it's not a problem
        if exc.response['Error']['Code'] == 'ConditionalCheckFailedException':
            success = True
        else:
            raise exc

    return success
