# Standard library
import aiohttp
import contextlib
from typing import (
    Optional,
    NamedTuple,
)

@contextlib.asynccontextmanager
async def request(
    *,
    headers: Optional[dict] = None,
    method: str,
    url: str,
):
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


async def stream_response(response: aiohttp.ClientResponse):
    while True:
        if chunk := await response.content.read(1024):
            yield chunk
        else:
            break
