# Third party libraries
from starlette.applications import (
    Starlette,
)
from starlette.routing import (
    Route,
)

# Local libraries
from nix_ipfs_node import (
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
            path='/{path:path}',
            endpoint=handlers.route_get,
            methods=['GET'],
        ),
        Route(
            path='/{path:path}',
            endpoint=handlers.route_head,
            methods=['HEAD'],
        ),
        Route(
            path='/{path:path}',
            endpoint=handlers.route_post,
            methods=['POST'],
        ),
    ],
)
