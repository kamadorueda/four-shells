"""Server routes."""

# Third party libraries
from starlette.responses import (
    Response,
)


async def on_shutdown() -> None:
    """Server shutdown script."""


async def on_startup() -> None:
    """Server startup script."""


async def home() -> Response:
    """Route for /."""
    return Response('Welcome!')


async def ping() -> Response:
    """Route for /ping."""
    return Response()
