"""Application route handlers."""

# Standard library
from typing import (
    Any,
    List,
)

# Third party libraries
from botocore.exceptions import (
    ClientError,
)
from boto3.dynamodb.conditions import (
    Attr,
    Key,
)
from starlette.requests import (
    Request,
)
from starlette.responses import (
    JSONResponse,
    Response,
)

# Local libraries
from server import (
    authz,
    persistence,
)
from server.utils.errors import (
    api_error_boundary,
)
from server.utils.security import (
    create_secret,
)


@api_error_boundary
# @authz.requires
async def namespace_associate(request: Request) -> Response:
    ns_id: str = request.path_params['id']


@api_error_boundary
@authz.requires_session
async def namespaces_create(request: Request) -> Response:
    account: str = request.session['email']
    name: str = request.path_params['name']
    ns_id: str = create_secret()
    token_admin: str = create_secret()
    token_read: str = create_secret()
    token_write: str = create_secret()

    try:
        await persistence.update(
            ConditionExpression=Attr('id').not_exists(),
            ExpressionAttributeNames={
                '#account': 'account',
                '#name': 'name',
                '#token_admin': 'token_admin',
                '#token_read': 'token_read',
                '#token_write': 'token_write',
            },
            ExpressionAttributeValues={
                ':account': account,
                ':name': name,
                ':token_admin': token_admin,
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
                '    #token_admin = :token_admin,'
                '    #token_read = :token_read,'
                '    #token_write = :token_write'
            ),
        )

    except ClientError as exc:
        raise exc

    return JSONResponse({'id': ns_id})


@api_error_boundary
@authz.requires_session
async def namespaces_delete(request: Request) -> Response:
    ns_id: str = request.path_params['id']

    try:
        success: bool = await persistence.delete(
            Key={
                'id': ns_id,
            },
            table=persistence.TableEnum.cachipfs_namespaces,
        )

    except ClientError as exc:
        raise exc

    return JSONResponse({'ok': success})


@api_error_boundary
@authz.requires_session
async def namespaces_get(request: Request) -> Response:
    ns_id: str = request.path_params['id']

    try:
        namespace = await persistence.get(
            Key={'id': ns_id},
            table=persistence.TableEnum.cachipfs_namespaces,
        )

    except ClientError as exc:
        raise exc

    return JSONResponse(namespace)


@api_error_boundary
@authz.requires_session
async def namespaces_list(request: Request) -> Response:
    account: str = request.session['email']

    try:
        namespaces: List[Any] = await persistence.query(
            IndexName='account__id',
            KeyConditionExpression=Key('account').eq(account),
            table=persistence.TableEnum.cachipfs_namespaces,
        )

    except ClientError as exc:
        raise exc

    return JSONResponse([
        {
            'id': namespace['id'],
            'name': namespace['name'],
        }
        for namespace in namespaces
    ])


@api_error_boundary
@authz.requires_session
async def namespace_rotate(request: Request) -> Response:
    ns_id: str = request.path_params['id']
    entity: str = request.path_params['entity']

    if entity not in {
        'token_admin',
        'token_read',
        'token_write',
    }:
        raise ValueError('Invalid token entity')

    try:
        await persistence.update(
            ExpressionAttributeNames={
                '#entity': entity,
            },
            ExpressionAttributeValues={
                ':entity': create_secret(),
            },
            Key={'id': ns_id},
            table=persistence.TableEnum.cachipfs_namespaces,
            UpdateExpression='SET #entity = :entity',
        )

    except ClientError as exc:
        raise exc

    return JSONResponse({'ok': True})
