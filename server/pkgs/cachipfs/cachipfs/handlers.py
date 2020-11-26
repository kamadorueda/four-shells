"""Application route handlers."""

# Standard library
from typing import (
    Optional,
)

# Third party libraries
from starlette.responses import (
    JSONResponse,
)
from starlette.requests import (
    Request,
)

# Local libraries
from cachipfs import (
    persistence,
)


async def on_shutdown() -> None:
    """Server shutdown script."""


async def on_startup() -> None:
    """Server startup script."""


async def api_delete_hash(request: Request) -> JSONResponse:
    """
    responses:
        200:
            description: Delete all hash associations.
            examples:
                ok: true
    """
    hash: str = request.path_params['hash']

    success = await persistence.delete(hash)

    return JSONResponse({'ok': success})


async def api_get_hash(request: Request) -> JSONResponse:
    """
    responses:
        200:
            description: Retrieve the CID associated to a hash.
            examples:
                cid: Qm...
    """
    hash: str = request.path_params['hash']

    cid: Optional[str] = await persistence.get(hash)

    return JSONResponse({'cid': cid})


async def api_set_hash(request: Request) -> JSONResponse:
    """
    responses:
        200:
            description: Associate a hash with a CID.
            examples:
                ok: true
    """
    cid: str = request.path_params['cid']
    hash: str = request.path_params['hash']

    success: bool = await persistence.set(hash, cid)

    return JSONResponse({'ok': success})
