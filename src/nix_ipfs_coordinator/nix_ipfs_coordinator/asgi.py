# Third party libraries
from starlette.applications import Starlette
from starlette.routing import Route

# Local libraries
from nix_ipfs_coordinator import (
    handlers,
)

# Constants
APP = Starlette(
    routes=[
        Route('/{path:path}', handlers.route),
    ],
)
