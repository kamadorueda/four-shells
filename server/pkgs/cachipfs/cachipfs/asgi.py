"""Routing of the server."""

# Third party libraries
from starlette.requests import (
    Request,
)
from starlette.routing import (
    Route,
    Router,
)

# Local libraries
import cachipfs.handlers

# Constants
APP = Router(
    routes=[
        Route(
            path='/',
            endpoint=cachipfs.handlers.home,
            methods=['GET'],
        ),
    ],
)
