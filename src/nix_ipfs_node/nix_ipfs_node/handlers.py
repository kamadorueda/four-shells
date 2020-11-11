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
)


async def route(request: Request):
    headers = dict(request.headers)
    method = request.method
    path = request.path_params['path']
    url = f'{config.SUBSTITUTER}/{path}'

    # Override host header with the proxied substituter
    headers['host'] = config.SUBSTITUTER_NETLOC

    async def streamer():
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(
                verify_ssl=False,
            ),
            timeout=aiohttp.ClientTimeout(
                total=60,
                connect=None,
                sock_read=None,
                sock_connect=None,
            ),
            trust_env=True,
        ) as session:
            async with session.request(
                headers=headers,
                method=method,
                url=url,
            ) as response:
                yield response.status

                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    yield chunk

    content = streamer()
    status_code = await content.asend(None)

    return StreamingResponse(
        content=content,
        media_type='application/octet-stream',
        status_code=status_code,
    )
