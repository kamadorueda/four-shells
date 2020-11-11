# Third party libraries
from starlette.applications import Starlette
from starlette.routing import Route

# Local libraries
from nix_ipfs_node.routes import (
    homepage,
)

# Constants
APP = Starlette(debug=True, routes=[
    Route('/', homepage),
])
