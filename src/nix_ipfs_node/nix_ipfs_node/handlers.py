# Standard library
import json
import os

# Third party libraries
from starlette.requests import (
    Request,
)
from starlette.responses import (
    Response,
)


async def route(request: Request):
    return Response("Hello world")
