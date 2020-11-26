"""Routing of the server."""

# Third party libraries
from starlette.routing import (
    Route,
)
from starlette.applications import (
    Starlette,
)

# Local libraries
from cachipfs import (
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
            path='/v1/hash/{hash:str}',
            endpoint=handlers.api_delete_hash,
            methods=['DELETE'],
        ),
        Route(
            path='/v1/hash/{hash:str}',
            endpoint=handlers.api_get_hash,
            methods=['GET'],
        ),
        Route(
            path='/v1/hash/{hash:str}/cid/{cid:str}',
            endpoint=handlers.api_set_hash,
            methods=['POST'],
        ),
    ],
)
