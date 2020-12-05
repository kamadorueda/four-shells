"""Application route handlers."""

# Standard library
import json

# Third party libraries
from authlib.integrations.starlette_client import (
    OAuth,
)
from starlette.requests import (
    Request,
)
from starlette.responses import (
    RedirectResponse,
    Response,
)
from starlette.schemas import (
    SchemaGenerator,
)

# Local libraries
from four_shells import (
    accounts,
    authz,
    config,
)

# Constants
OAUTH = OAuth()
OAUTH.register(
    name='google',
    client_id=config.GOOGLE_OAUTH_CLIENT_ID_SERVER,
    client_secret=config.GOOGLE_OAUTH_SECRET_SERVER,
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


def index(request: Request) -> Response:
    return config.TPL.TemplateResponse('react.html', {
        'js': config.from_cdn('/static/index.js'),
        'globals': config.get_globals(request),
        'request': request,
    })


@authz.requires_session_sync
def console(request: Request) -> Response:
    return config.TPL.TemplateResponse('react.html', {
        'js': config.from_cdn('/static/console.js'),
        'globals': config.get_globals(request),
        'request': request,
    })


def docs(request: Request) -> Response:
    return config.TPL.TemplateResponse('react.html', {
        'js': config.from_cdn('/static/docs.js'),
        'globals': config.get_globals(request),
        'request': request,
    })


async def oauth_google_start(request: Request) -> Response:
    return await OAUTH.google.authorize_redirect(
        request,
        request.url_for('oauth_google_finish'),
    )


async def oauth_google_finish(request: Request) -> Response:
    token = await OAUTH.google.authorize_access_token(request)
    data = await OAUTH.google.parse_id_token(request, token)
    email = data['email'].lower()

    if await accounts.ensure_account_exists(email=email):
        request.session['email'] = email
        return RedirectResponse('/console/')

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
