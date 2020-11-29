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
PATHS_NAR_INFO = [
    '/{drv_hash:str}.narinfo',
]
PATHS_NAR_XZ = [
    '/nar/{nar_xz_hash:str}.nar.xz',
]


APP = Starlette(
    on_startup=[
        handlers.on_startup,
    ],
    on_shutdown=[
        handlers.on_shutdown,
    ],
    routes=[
        # Handle possible .narinfo requests
        *(
            Route(path, handlers.proxy_as_narinfo, methods=['GET'])
            for path in PATHS_NAR_INFO
        ),
        # Handle possible .nar.xz requests
        *(
            Route(path, handlers.proxy_as_nar_xz, methods=['GET'])
            for path in PATHS_NAR_XZ
        ),
        # Base case, just proxy to upstream
        Route('/{path:path}', handlers.proxy_to_substituter),
    ],
)
