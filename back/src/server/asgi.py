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
import config.server
import server.handlers
import server.cachipfs.handlers


# Constants
APP = Starlette(
    middleware=[
        Middleware(
            cls=SessionMiddleware,
            https_only=config.server.PRODUCTION,
            max_age=config.server.SESSION_DURATION,
            same_site='lax',
            secret_key=config.server.SESSION_SECRET,
            session_cookie=config.server.SESSION_COOKIE,
        ),
    ],
    on_startup=[
        server.handlers.on_startup,
    ],
    on_shutdown=[
        server.handlers.on_shutdown,
    ],
    routes=[
        Route(
            endpoint=server.cachipfs.handlers.namespace_associate,
            methods=['POST'],
            path='/api/v1/cachipfs/namespace/{id:str}/associate',
        ),
        Route(
            endpoint=server.cachipfs.handlers.namespace_rotate,
            methods=['POST'],
            path='/api/v1/cachipfs/namespace/{id:str}/rotate/{entity:str}',
        ),
        Route(
            endpoint=server.cachipfs.handlers.namespaces_create,
            methods=['POST'],
            path='/api/v1/cachipfs/namespace/{name:str}',
        ),
        Route(
            endpoint=server.cachipfs.handlers.namespaces_delete,
            methods=['DELETE'],
            path='/api/v1/cachipfs/namespace/{id:str}',
        ),
        Route(
            endpoint=server.cachipfs.handlers.namespaces_get,
            methods=['GET'],
            path='/api/v1/cachipfs/namespace/{id:str}',
        ),
        Route(
            endpoint=server.cachipfs.handlers.namespaces_list,
            methods=['GET'],
            path='/api/v1/cachipfs/namespaces',
        ),
        Route(
            endpoint=server.handlers.cachipfs,
            methods=['GET'],
            path='/cachipfs{path:path}',
        ),
        Route(
            endpoint=server.handlers.docs,
            methods=['GET'],
            path='/docs{path:path}',
        ),
        Route(
            endpoint=server.handlers.nixdb,
            methods=['GET'],
            path='/nixdb{path:path}',
        ),
        Route(
            endpoint=server.handlers.oauth_google_start,
            methods=['GET'],
            path='/oauth/google/start',
        ),
        Route(
            endpoint=server.handlers.oauth_google_finish,
            methods=['GET'],
            name='oauth_google_finish',
            path='/oauth/google/finish',
        ),
        Route(
            endpoint=server.handlers.ping,
            methods=['GET'],
            path='/ping',
        ),
        Route(
            endpoint=server.handlers.schema,
            methods=['GET'],
            path='/schema',
        ),
        Route(
            endpoint=server.handlers.index,
            methods=['GET'],
            path='/{path:path}',
        ),
    ],
)
