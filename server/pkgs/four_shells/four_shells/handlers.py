"""Application route handlers."""

# Third party libraries
from starlette.requests import (
    Request,
)
from starlette.responses import (
    Response,
)
from starlette.schemas import (
    SchemaGenerator,
)

# Constants
SCHEMA = SchemaGenerator({
    "openapi": "3.0.0",
    "info": {
        "title": "Four Shells",
    },
})


async def on_shutdown() -> None:
    """Server shutdown script."""


async def on_startup() -> None:
    """Server startup script."""


async def home(request: Request) -> Response:
    """Route for /."""
    return Response('Welcome!')


async def ping(request: Request) -> Response:
    """
    responses:
      200:
        description: Ping the server in order to perform a health check.
    """
    return Response()


def schema(request: Request) -> Response:
    return SCHEMA.OpenAPIResponse(request)
