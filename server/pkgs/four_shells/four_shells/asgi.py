"""Routing of the server."""

# Third party libraries
from starlette.applications import (
    Starlette,
)
from starlette.routing import (
    Mount,
    Route,
)


# Local libraries
import cachipfs.asgi
import four_shells.handlers


# Constants
APP = Starlette(
    on_startup=[
        four_shells.handlers.on_startup,
    ],
    on_shutdown=[
        four_shells.handlers.on_shutdown,
    ],
    routes=[
        Route(
            endpoint=four_shells.handlers.home,
            include_in_schema=False,
            methods=['GET'],
            path='/',
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
        Route(
            path='/schema',
            endpoint=four_shells.handlers.schema,
            include_in_schema=False,
            methods=['GET'],
        )
    ],
)
