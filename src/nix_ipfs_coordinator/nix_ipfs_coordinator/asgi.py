# Third party libraries
from starlette.applications import Starlette
from starlette.routing import Route

# Local libraries
from nix_ipfs_coordinator import (
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
            path='/api/host/{host:str}/hash/{hash:str}',
            endpoint=handlers.api_host___hash____delete,
            methods=['DELETE'],
        ),
        Route(
            path='/api/host/{host:str}/hash/{hash:str}',
            endpoint=handlers.api_host___hash____get,
            methods=['GET'],
        ),
        Route(
            path='/api/host/{host:str}/hash/{hash:str}/cid/{cid:str}',
            endpoint=handlers.api_host___hash____cid___post,
            methods=['POST'],
        ),
    ],
)
