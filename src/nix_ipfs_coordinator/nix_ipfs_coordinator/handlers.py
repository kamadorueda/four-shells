# Standard library
import json
import os

# Third party libraries
import aiohttp
from starlette.requests import (
    Request,
)
from starlette.responses import (
    Response,
    StreamingResponse,
)

# Local libraries
from nix_ipfs_coordinator import (
    config,
)


async def route(request: Request):
    return
