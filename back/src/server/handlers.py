# Third party libraries
from authlib.integrations.starlette_client import (
    OAuth,
)
from server.utils.data import (
    get_ttl,
    json_cast,
)
from starlette.requests import (
    Request,
)
from starlette.responses import (
    JSONResponse,
    RedirectResponse,
    Response,
)
from starlette.schemas import (
    SchemaGenerator,
)

# Local libraries
import config.server
from server import (
    accounts,
    authz,
    persistence,
)
from server.utils.errors import (
    api_error_boundary,
)

# Constants
OAUTH = OAuth()
OAUTH.register(
    name='google',
    client_id=config.server.GOOGLE_OAUTH_CLIENT_ID,
    client_secret=config.server.GOOGLE_OAUTH_SECRET,
    server_metadata_url=(
        'https://accounts.google.com/.well-known/openid-configuration'
    ),
    client_kwargs={
        'scope': 'email'
    },
)
SCHEMA = SchemaGenerator({
    "openapi": "3.0.0",
    "info": {
        "title": "Four Shells",
    },
})


async def on_shutdown() -> None:
    """Server shutdown script."""


async def on_startup() -> None:
    """Server startup script."""


@api_error_boundary
@authz.requires_session
async def api_v1_me(request: Request) -> Response:
    namespace = await persistence.get(
        Key={'email': request.session['email']},
        table=persistence.TableEnum.accounts,
    )

    return JSONResponse(json_cast(namespace))


@api_error_boundary
async def api_v1_cachipfs_publish(request: Request) -> Response:
    data = await authz.validate_cachipfs_api_token(request)

    cid: str = request.path_params['cid']
    email: str = data.email
    nar_path: str = request.path_params['nar_path']

    success = await persistence.update(
        ExpressionAttributeNames={
            '#cid': 'cid',
            '#ttl': 'ttl',
        },
        ExpressionAttributeValues={
            ':cid': cid,
            ':ttl': get_ttl(2419200),
        },
        Key={
            'email': email,
            'nar_path': nar_path,
        },
        table=persistence.TableEnum.cachipfs_objects,
        UpdateExpression=(
            'SET #cid = :cid,'
            '    #ttl = :ttl'
        ),
    )

    return JSONResponse({'ok': success})


def cachipfs(request: Request) -> Response:
    return config.server.TPL.TemplateResponse('react.html', {
        'js': config.server.from_cdn('/static/cachipfs.js'),
        'globals': config.server.get_globals(request),
        'request': request,
    })


def index(request: Request) -> Response:
    return config.server.TPL.TemplateResponse('react.html', {
        'js': config.server.from_cdn('/static/index.js'),
        'globals': config.server.get_globals(request),
        'request': request,
    })


def docs(request: Request) -> Response:
    return config.server.TPL.TemplateResponse('react.html', {
        'js': config.server.from_cdn('/static/docs.js'),
        'globals': config.server.get_globals(request),
        'request': request,
    })


def nixdb(request: Request) -> Response:
    return config.server.TPL.TemplateResponse('react.html', {
        'js': config.server.from_cdn('/static/nixdb.js'),
        'globals': config.server.get_globals(request),
        'request': request,
    })


async def oauth_google_start(request: Request) -> Response:
    request.session['next_url'] = request.query_params['next']

    return await OAUTH.google.authorize_redirect(
        request,
        request.url_for('oauth_google_finish'),
    )


async def oauth_google_finish(request: Request) -> Response:
    token = await OAUTH.google.authorize_access_token(request)
    data = await OAUTH.google.parse_id_token(request, token)
    email = data['email'].lower()
    next_url = request.session.pop('next_url', '')

    if next_url not in {'/cachipfs/dashboard'}:
        raise ValueError('Invalid next URL')

    if await accounts.ensure_account_exists(email=email):
        request.session['email'] = email
        return RedirectResponse(next_url)

    raise Exception(f'Unable to create account for email: {email}')


async def ping(request: Request) -> Response:
    """
    responses:
      200:
        description: Ping the server in order to perform a health check.
    """
    return Response()


def schema(request: Request) -> Response:
    response = SCHEMA.OpenAPIResponse(request)
    return Response(response.body, media_type='text/plain')
