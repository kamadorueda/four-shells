# Standard library
import contextlib
from typing import (
    Any,
    Dict,
    NamedTuple,
    Optional,
)

# Third party libraries
import aiohttp

# Local libraries
import config.cachipfs
from logs import (
    log,
)

# Constants
ENDPOINT: str = 'https://4shells.com'
# ENDPOINT: str = 'http://localhost:8400'

class Error(Exception):
    pass


@contextlib.asynccontextmanager
async def api(
    *,
    headers: Dict[str, str],
    method: str,
    params: Optional[Dict[str, str]] = None,
    path: str,
) -> Dict[str, Any]:
    async with aiohttp.ClientSession() as session:
        async with session.request(
            headers=headers,
            method=method,
            params=params,
            url=f'{ENDPOINT}{path}',
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
    *,
    method: str,
    params: Optional[Dict[str, str]] = None,
    path: str,
) -> Dict[str, Any]:
    async with api(
        headers={
            'authorization': config.cachipfs.API_TOKEN,
        },
        method=method,
        params=params,
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

    await log('info', 'Announcing to cachipfs cid: %s', cid)

    async with api_cachipfs(
        method='POST',
        params=dict(
            cid=cid,
            nar_path=nar_path,
        ),
        path=f'/api/v1/cachipfs/objects'
    ):
        pass
