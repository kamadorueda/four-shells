# Standard library
import contextlib
from typing import (
    Any,
    Dict,
    NamedTuple,
)
from urllib.parse import (
    quote_plus,
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
    headers: Dict[str, str],
    method: str,
    path: str,
) -> Dict[str, Any]:
    async with aiohttp.ClientSession() as session:
        async with session.request(
            headers=headers,
            method=method,
            url=f'https://4shells.com{path}',
        ) as response:
            try:
                data = await response.json()
            except aiohttp.ClientError:
                await log('error', '4shells API: %s', await response.text())
                data = {}

            if 'error' in data:
                await log('error', '%s', data['error'])
                raise Error(data['error'])

            yield data


@contextlib.asynccontextmanager
async def api_cachipfs(
    method: str,
    path: str,
) -> Dict[str, Any]:
    async with api(
        headers={
            'authorization': config.cachipfs.API_TOKEN,
        },
        method=method,
        path=path,
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


async def api_v1_cachipfs_objects_post(
    cid: str,
    nar_path: str,
) -> None:
    cid = quote_plus(cid)
    nar_path = quote_plus(nar_path)

    await log('info', 'Announcing to cachipfs cid: %s', cid)

    async with api_cachipfs(
        method='POST',
        path=f'/api/v1/cachipfs/objects/{nar_path}/{cid}',
    ):
        pass
