"""Routing of the server."""

# Third party libraries
# Local libraries
import config.server
import server.handlers
from starlette.applications import (
    Starlette,
)
from starlette.middleware import (
    Middleware,
)
from starlette.middleware.sessions import (
    SessionMiddleware,
)
from starlette.routing import (
    Route,
)

# Constants
APP = Starlette(
    middleware=[
        Middleware(
            cls=SessionMiddleware,
            https_only=config.server.PRODUCTION,
            max_age=config.server.SESSION_DURATION,
            same_site="lax",
            secret_key=config.server.SESSION_SECRET,
            session_cookie=config.server.SESSION_COOKIE,
        ),
    ],
    on_startup=[
        server.handlers.on_startup,
    ],
    on_shutdown=[
        server.handlers.on_shutdown,
    ],
    routes=[
        Route(
            endpoint=server.handlers.ads,
            methods=["GET"],
            path="/ads.txt",
        ),
        Route(
            endpoint=server.handlers.docs,
            methods=["GET"],
            path="/docs{path:path}",
        ),
        Route(
            endpoint=server.handlers.nixdb,
            methods=["GET"],
            path="/nixdb{path:path}",
        ),
        Route(
            endpoint=server.handlers.ping,
            methods=["GET"],
            path="/ping",
        ),
        Route(
            endpoint=server.handlers.robots,
            methods=["GET"],
            path="/robots.txt",
        ),
        Route(
            endpoint=server.handlers.schema,
            methods=["GET"],
            path="/schema",
        ),
        Route(
            endpoint=server.handlers.sitemap,
            methods=["GET"],
            path="/sitemap-{index:int}.xml",
        ),
        Route(
            endpoint=server.handlers.sitemap,
            methods=["GET"],
            path="/sitemapindex-{index:int}.xml",
        ),
        Route(
            endpoint=server.handlers.index,
            methods=["GET"],
            path="/{path:path}",
        ),
    ],
)
