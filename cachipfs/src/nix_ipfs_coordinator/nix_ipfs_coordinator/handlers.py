# Standard library
from typing import (
    Optional,
)

# Third party libraries
import aioredis
from starlette.requests import (
    Request,
)
from starlette.responses import (
    JSONResponse,
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


async def api_host___hash____delete(request: Request) -> JSONResponse:
    hash: str = request.path_params['hash']
    host: str = request.path_params['host']

    success: bool = await persistence.delete(host, hash)

    return JSONResponse({'success': success})


async def api_host___hash____get(request: Request) -> JSONResponse:
    hash: str = request.path_params['hash']
    host: str = request.path_params['host']

    cid: Optional[str] = await persistence.get(host, hash)

    return JSONResponse({'cid': cid})


async def api_host___hash____cid___post(request: Request) -> JSONResponse:
    cid: str = request.path_params['cid']
    hash: str = request.path_params['hash']
    host: str = request.path_params['host']

    success: bool = await persistence.set(host, hash, cid)

    return JSONResponse({'success': success})
