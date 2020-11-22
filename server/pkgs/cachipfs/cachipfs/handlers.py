"""Application route handlers."""

# Third party libraries
from starlette.requests import (
    Request,
)
from starlette.responses import (
    Response,
)


async def on_shutdown() -> None:
    """Server shutdown script."""


async def on_startup() -> None:
    """Server startup script."""


async def home(request: Request) -> Response:
    """Route for /."""
    return Response('Welcome!')
