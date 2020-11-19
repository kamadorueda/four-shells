# Third party libraries
from starlette.requests import (
    Request,
)
from starlette.responses import (
    Response,
)


async def on_shutdown() -> None:
    pass


async def on_startup() -> None:
    pass


async def ping(request: Request) -> Response:
    return Response()
