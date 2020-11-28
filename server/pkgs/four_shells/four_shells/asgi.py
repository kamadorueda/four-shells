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
    Mount,
    Route,
)


# Local libraries
import cachipfs.asgi
from four_shells import (
    config,
    handlers,
)


# Constants
APP = Starlette(
    middleware=[
        Middleware(
            cls=SessionMiddleware,
            https_only=config.PRODUCTION,
            max_age=config.SESSION_DURATION,
            same_site='lax',
            secret_key=config.SESSION_SECRET,
            session_cookie=config.SESSION_COOKIE,
        ),
    ],
    on_startup=[
        handlers.on_startup,
    ],
    on_shutdown=[
        handlers.on_shutdown,
    ],
    routes=[
        Mount(
            app=cachipfs.asgi.APP,
            path='/api/cachipfs',
        ),
        Route(
            endpoint=handlers.console,
            methods=['GET'],
            path='/console/{path:path}',
        ),
        Route(
            endpoint=handlers.oauth_google_start,
            methods=['GET'],
            path='/oauth/google/start',
        ),
        Route(
            endpoint=handlers.oauth_google_finish,
            methods=['GET'],
            name='oauth_google_finish',
            path='/oauth/google/finish',
        ),
        Route(
            endpoint=handlers.ping,
            methods=['GET'],
            path='/ping',
        ),
        Route(
            endpoint=handlers.schema,
            methods=['GET'],
            path='/schema',
        ),
        Route(
            endpoint=handlers.index,
            methods=['GET'],
            path='/{path:path}',
        ),
    ],
)
