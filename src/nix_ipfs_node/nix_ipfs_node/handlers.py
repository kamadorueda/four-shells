# Standard library
import json
import os

# Third party libraries
import aiohttp
from starlette.requests import (
    Request,
)
from starlette.responses import (
    Response,
    StreamingResponse,
)

# Local libraries
from nix_ipfs_node import (
    config,
    http,
)


async def route(request: Request):
    headers = dict(request.headers)
    method = request.method
    path = request.path_params['path']
    url = f'{config.SUBSTITUTER}/{path}'

    # Override host header with the proxied substituter
    headers['host'] = config.SUBSTITUTER_NETLOC

    async def generate_content():
        async with http.request(
            headers=headers,
            method=method,
            url=url,
        ) as response:
            yield response.status

            async for chunk in http.stream_response(response):
                yield chunk

    content_generator = generate_content()
    status_code = await content_generator.asend(None)

    return StreamingResponse(
        content=content_generator,
        media_type='application/octet-stream',
        status_code=status_code,
    )
