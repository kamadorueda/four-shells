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
            secret_key=config.SERVER_STATE_COOKIE_SECRET,
            session_cookie='four_shells_state',
        ),
    ],
    on_startup=[
        handlers.on_startup,
    ],
    on_shutdown=[
        handlers.on_shutdown,
    ],
    routes=[
        Route(
            endpoint=handlers.index,
            methods=['GET'],
            path='/',
        ),
        Route(
            endpoint=handlers.console,
            methods=['GET'],
            name='console',
            path='/console',
        ),
        Mount(
            app=cachipfs.asgi.APP,
            path='/api/cachipfs',
        ),
        Route(
            endpoint=handlers.oauth_google_init,
            methods=['GET'],
            path='/oauth/google/init',
        ),
        Route(
            endpoint=handlers.oauth_google_receive,
            methods=['GET'],
            name='oauth_google_receive',
            path='/oauth/google/receive',
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

    ],
)
