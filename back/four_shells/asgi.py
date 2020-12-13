"""Routing of the server."""

# Third party libraries
from starlette.applications import (
    Starlette,
)
from starlette.middleware import (
    Middleware,
)
from starlette.middleware.sessions import (
    SessionMiddleware,
)
from starlette.routing import (
    Route,
)


# Local libraries
import four_shells.config
import four_shells.handlers
import four_shells.cachipfs.handlers


# Constants
APP = Starlette(
    middleware=[
        Middleware(
            cls=SessionMiddleware,
            https_only=four_shells.config.PRODUCTION,
            max_age=four_shells.config.SESSION_DURATION,
            same_site='lax',
            secret_key=four_shells.config.SESSION_SECRET,
            session_cookie=four_shells.config.SESSION_COOKIE,
        ),
    ],
    on_startup=[
        four_shells.handlers.on_startup,
    ],
    on_shutdown=[
        four_shells.handlers.on_shutdown,
    ],
    routes=[
        Route(
            endpoint=four_shells.cachipfs.handlers.namespace_associate,
            methods=['POST'],
            path='/api/v1/cachipfs/namespace/{id:str}/associate',
        ),
        Route(
            endpoint=four_shells.cachipfs.handlers.namespace_rotate,
            methods=['POST'],
            path='/api/v1/cachipfs/namespace/{id:str}/rotate/{entity:str}',
        ),
        Route(
            endpoint=four_shells.cachipfs.handlers.namespaces_create,
            methods=['POST'],
            path='/api/v1/cachipfs/namespace/{name:str}',
        ),
        Route(
            endpoint=four_shells.cachipfs.handlers.namespaces_delete,
            methods=['DELETE'],
            path='/api/v1/cachipfs/namespace/{id:str}',
        ),
        Route(
            endpoint=four_shells.cachipfs.handlers.namespaces_get,
            methods=['GET'],
            path='/api/v1/cachipfs/namespace/{id:str}',
        ),
        Route(
            endpoint=four_shells.cachipfs.handlers.namespaces_list,
            methods=['GET'],
            path='/api/v1/cachipfs/namespaces',
        ),
        Route(
            endpoint=four_shells.handlers.cachipfs,
            methods=['GET'],
            path='/cachipfs{path:path}',
        ),
        Route(
            endpoint=four_shells.handlers.docs,
            methods=['GET'],
            path='/docs{path:path}',
        ),
        Route(
            endpoint=four_shells.handlers.nixdb,
            methods=['GET'],
            path='/nixdb{path:path}',
        ),
        Route(
            endpoint=four_shells.handlers.oauth_google_start,
            methods=['GET'],
            path='/oauth/google/start',
        ),
        Route(
            endpoint=four_shells.handlers.oauth_google_finish,
            methods=['GET'],
            name='oauth_google_finish',
            path='/oauth/google/finish',
        ),
        Route(
            endpoint=four_shells.handlers.ping,
            methods=['GET'],
            path='/ping',
        ),
        Route(
            endpoint=four_shells.handlers.schema,
            methods=['GET'],
            path='/schema',
        ),
        Route(
            endpoint=four_shells.handlers.index,
            methods=['GET'],
            path='/{path:path}',
        ),
    ],
)
