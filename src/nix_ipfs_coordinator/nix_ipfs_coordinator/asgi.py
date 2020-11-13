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
            path='/api/nix_nar_xz_hash/{nix_nar_xz_hash:str}',
            endpoint=handlers.api_nix_nar_xz_hash_delete,
            methods=['DELETE'],
        ),
        Route(
            path='/api/nix_nar_xz_hash/{nix_nar_xz_hash:str}',
            endpoint=handlers.api_nix_nar_xz_hash_get,
            methods=['GET'],
        ),
        Route(
            path='/api/nix_nar_xz_hash/{nix_nar_xz_hash:str}/{ipfs_cid:str}',
            endpoint=handlers.api_nix_nar_xz_hash_post,
            methods=['POST'],
        ),
    ],
)
