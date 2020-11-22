"""Routing of the server."""

# Third party libraries
from starlette.routing import (
    Mount,
    Route,
    Router,
)

# Local libraries
import cachipfs.asgi
import four_shells.handlers


# Constants
APP = Router(
    on_startup=[
        four_shells.handlers.on_startup,
    ],
    on_shutdown=[
        four_shells.handlers.on_shutdown,
    ],
    routes=[
        Route(
            path='/',
            endpoint=four_shells.handlers.home,
            methods=['GET'],
        ),
        Mount(
            app=cachipfs.asgi.APP,
            path='/cachipfs',
        ),
        Route(
            path='/ping',
            endpoint=four_shells.handlers.ping,
            methods=['GET'],
        ),
    ],
)
