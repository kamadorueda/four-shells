"""Application route handlers."""

# Third party libraries
from botocore.exceptions import (
    ClientError,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from starlette.requests import (
    Request,
)
from starlette.responses import (
    JSONResponse,
    Response,
)

# Local libraries
from four_shells import (
    authz,
    persistence,
)
from four_shells.utils import (
    create_secret,
)


@authz.requires_session
async def namespaces_create(request: Request) -> Response:
    account: str = request.session['email']
    name: str = request.path_params['name']
    ns_id: str = create_secret()
    token_read: str = create_secret()
    token_write: str = create_secret()

    try:
        await persistence.update(
            ConditionExpression=Attr('id').not_exists(),
            ExpressionAttributeNames={
                '#account': 'account',
                '#name': 'name',
                '#token_read': 'token_read',
                '#token_write': 'token_write',
            },
            ExpressionAttributeValues={
                ':account': account,
                ':name': name,
                ':token_read': token_read,
                ':token_write': token_write,
            },
            Key={
                'id': ns_id,
            },
            table=persistence.TableEnum.cachipfs_namespaces,
            UpdateExpression=(
                'SET #account = :account,'
                '    #name = :name,'
                '    #token_read = :token_read,'
                '    #token_write = :token_write'
            ),
        )

    except ClientError as exc:
        raise exc

    return JSONResponse({
        'id': ns_id,
        'token_read': token_read,
        'token_write': token_write,
    })
