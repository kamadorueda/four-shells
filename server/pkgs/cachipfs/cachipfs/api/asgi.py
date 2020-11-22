"""Routing of the server."""

# Third party libraries
from starlette.routing import (
    Route,
    Router,
)

# Local libraries
from cachipfs.api import (
    handlers,
)

# Constants
APP = Router(
    routes=[
        Route(
            path='/hash/{hash:str}',
            endpoint=handlers.api_delete_hash,
            methods=['DELETE'],
        ),
        Route(
            path='/hash/{hash:str}',
            endpoint=handlers.api_get_hash,
            methods=['GET'],
        ),
        Route(
            path='/hash/{hash:str}/cid/{cid:str}',
            endpoint=handlers.api_set_hash,
            methods=['POST'],
        ),
    ],
)
