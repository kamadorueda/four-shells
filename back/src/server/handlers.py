# Standard library
# Third party libraries
# Local libraries
import config.server
import os
from server.utils.data import (
    get_ttl,
    json_cast,
)
from server.utils.errors import (
    api_error_boundary,
)
from starlette.requests import (
    Request,
)
from starlette.responses import (
    FileResponse,
    JSONResponse,
    RedirectResponse,
    Response,
)
from starlette.schemas import (
    SchemaGenerator,
)

# Constants
SCHEMA = SchemaGenerator(
    {
        "openapi": "3.0.0",
        "info": {
            "title": "Four Shells",
        },
    }
)


async def on_shutdown() -> None:
    """Server shutdown script."""


async def on_startup() -> None:
    """Server startup script."""


def index(request: Request) -> Response:
    return config.server.TPL.TemplateResponse(
        "react.html",
        {
            "icon": config.server.from_cdn("/icon.ico"),
            "js": config.server.from_cdn("/front/index.js"),
            "globals": config.server.get_globals(request),
            "request": request,
        },
    )


def docs(request: Request) -> Response:
    return config.server.TPL.TemplateResponse(
        "react.html",
        {
            "icon": config.server.from_cdn("/icon.ico"),
            "js": config.server.from_cdn("/front/docs.js"),
            "globals": config.server.get_globals(request),
            "request": request,
        },
    )


def nixdb(request: Request) -> Response:
    return config.server.TPL.TemplateResponse(
        "react.html",
        {
            "icon": config.server.from_cdn("/icon.ico"),
            "js": config.server.from_cdn("/front/nixdb.js"),
            "globals": config.server.get_globals(request),
            "request": request,
        },
    )


def ads(_: Request) -> Response:
    return FileResponse(f"{config.server.SRC_BACK}/ads.txt")


def robots(_: Request) -> Response:
    return FileResponse(f"{config.server.SRC_BACK}/robots.txt")


def sitemap(request: Request) -> Response:
    return FileResponse(f"{config.server.SRC_BACK}/sitemap{request.url.path}")


async def ping(request: Request) -> Response:
    """
    responses:
      200:
        description: Ping the server in order to perform a health check.
    """
    return Response()


def schema(request: Request) -> Response:
    response = SCHEMA.OpenAPIResponse(request)
    return Response(response.body, media_type="text/plain")
