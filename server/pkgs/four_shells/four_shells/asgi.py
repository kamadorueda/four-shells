# Third party libraries
from starlette.applications import Starlette
from starlette.routing import Route

# Local libraries
from four_shells import (
    handlers,
)

# Constants
APP = Starlette(
    on_startup=[
        handlers.on_startup,
    ],
    on_shutdown=[
        handlers.on_shutdown,
    ],
    routes=[
        Route(
            path='/',
            endpoint=handlers.home,
            methods=['GET'],
        ),
        Route(
            path='/ping',
            endpoint=handlers.ping,
            methods=['GET'],
        ),
    ],
)
