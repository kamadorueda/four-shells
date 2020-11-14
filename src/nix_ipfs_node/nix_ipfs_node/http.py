# Standard library
import aiohttp
import contextlib
from typing import (
    AsyncIterable,
    Optional,
)

# Third party libraries
from starlette.datastructures import (
    Headers,
)
from starlette.responses import (
    StreamingResponse,
)

@contextlib.asynccontextmanager
async def request(
    *,
    headers: Optional[dict] = None,
    method: str,
    url: str,
) -> aiohttp.ClientResponse:
    connector = aiohttp.TCPConnector(verify_ssl=False)
    timeout = aiohttp.ClientTimeout(connect=None, total=60, sock_connect=None, sock_read=None)

    async with aiohttp.ClientSession(
        connector=connector,
        timeout=timeout,
        trust_env=True,
    ) as session:
        async with session.request(
            headers=headers,
            method=method,
            url=url,
        ) as response:
            yield response


async def stream_response(
    *,
    chunk_size: int = 1024,
    response: aiohttp.ClientResponse,
) -> AsyncIterable[bytes]:
    while True:
        if chunk := await response.content.read(chunk_size):
            yield chunk
        else:
            break


async def stream_from_substituter(
    headers: Headers,
    method: str,
    url: str,
) -> StreamingResponse:

    async def generate_content():
        async with request(
            headers=headers,
            method=method,
            url=url,
        ) as response:
            yield response.status

            async for chunk in stream_response(response=response):
                yield chunk

    content_generator = generate_content()
    status_code = await content_generator.asend(None)

    return StreamingResponse(
        content=content_generator,
        media_type='application/octet-stream',
        status_code=status_code,
    )
