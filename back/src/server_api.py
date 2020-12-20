# Standard library
import contextlib
from typing import (
    Any,
    Dict,
    NamedTuple,
)

# Third party libraries
import aiohttp

# Local libraries
import config.cachipfs
from logs import (
    log,
)


class Error(Exception):
    pass


@contextlib.asynccontextmanager
async def api(
    method: str,
    path: str,
    *args: Any,
    **kwargs: Any,
) -> Dict[str, Any]:
    async with aiohttp.ClientSession() as session:
        async with session.request(
            method=method,
            url=f'https://4shells.com{path}',
            *args,
            **kwargs,
        ) as response:
            data = await response.json()

            if 'error' in data:
                await log('error', '%s', data['error'])
                raise Error(data['error'])

            yield data


@contextlib.asynccontextmanager
async def api_cachipfs(
    method: str,
    path: str,
    *args: Any,
    **kwargs: Any,
) -> Dict[str, Any]:
    async with api(
        headers={
            'authorization': config.cachipfs.API_TOKEN,
        },
        method=method,
        path=path,
        *args, **kwargs
    ) as data:
        yield data


class V1CachipfsConfigGet(NamedTuple):
    cachipfs_encryption_key: str
    email: str


async def api_v1_cachipfs_config_get() -> V1CachipfsConfigGet:
    async with api_cachipfs(
        method='GET',
        path='/api/v1/cachipfs/config',
    ) as data:
        return V1CachipfsConfigGet(
            cachipfs_encryption_key=data['cachipfs_encryption_key'],
            email=data['email'],
        )
