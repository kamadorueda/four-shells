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


async def api_nix_nar_xz_hash_delete(request: Request) -> JSONResponse:
    nix_nar_xz_hash: str = request.path_params['nix_nar_xz_hash']

    success: bool = await persistence.delete(nix_nar_xz_hash)

    return JSONResponse({'success': success})


async def api_nix_nar_xz_hash_get(request: Request) -> JSONResponse:
    nix_nar_xz_hash: str = request.path_params['nix_nar_xz_hash']

    ipfs_cid: Optional[str] = await persistence.get(nix_nar_xz_hash)

    return JSONResponse({'ipfs_cid': ipfs_cid})


async def api_nix_nar_xz_hash_post(request: Request) -> JSONResponse:
    nix_nar_xz_hash: str = request.path_params['nix_nar_xz_hash']
    ipfs_cid: str = request.path_params['ipfs_cid']

    success: bool = await persistence.set(nix_nar_xz_hash, ipfs_cid)

    return JSONResponse({'success': success})
