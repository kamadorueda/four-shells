# Standard library
import json
import os

# Third party libraries
import aioredis
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
    persistence,
)


async def on_shutdown() -> None:
    persistence.CONNECTION.close()
    await persistence.CONNECTION.wait_closed()


async def on_startup() -> None:
    persistence.CONNECTION = await aioredis.create_redis_pool(
        config.DATA_STORE_STRING,
        minsize=1,
        maxsize=10,
        timeout=10,
    )


async def api_nix_nar_xz_hash_delete(request: Request) -> Response:
    return


async def api_nix_nar_xz_hash_get(request: Request) -> Response:
    return


async def api_nix_nar_xz_hash_post(request: Request) -> Response:
    return
