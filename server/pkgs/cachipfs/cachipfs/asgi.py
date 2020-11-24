"""Routing of the server."""

# Third party libraries
from starlette.routing import (
    Mount,
    Route,
    Router,
)

# Local libraries
import cachipfs.handlers
import cachipfs.api.asgi

# Constants
APP = Router(
    routes=[
        Route(
            path='/',
            endpoint=cachipfs.handlers.home,
            methods=['GET'],
        ),
        Mount(
            path='/api/v1',
            app=cachipfs.api.asgi.APP,
        )
    ],
)
