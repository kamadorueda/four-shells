# Standard library
from typing import (
    Any,
    Dict,
    NamedTuple,
    Optional,
)
from aioextensions import (
    rate_limited,
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
DELAY_BETWEEN_REQUESTS_IN_SECONDS: int = 0


class Error(Exception):
    pass


async def api_no_rate_limited(
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

            return data


@rate_limited(
    max_calls=1,
    max_calls_period=DELAY_BETWEEN_REQUESTS_IN_SECONDS,
    min_seconds_between_calls=DELAY_BETWEEN_REQUESTS_IN_SECONDS,
)
async def api(
    *,
    headers: Dict[str, str],
    method: str,
    params: Optional[Dict[str, str]] = None,
    path: str,
) -> Dict[str, Any]:
    return await api_no_rate_limited(
        headers=headers,
        method=method,
        params=params,
        path=path,
    )


class V1CachipfsConfigGet(NamedTuple):
    cachipfs_encryption_key: str
    email: str


async def api_v1_cachipfs_config_get() -> V1CachipfsConfigGet:
    data = await api_no_rate_limited(
        headers={'authorization': config.cachipfs.API_TOKEN},
        method='GET',
        path='/api/v1/cachipfs/config',
    )

    return V1CachipfsConfigGet(
        cachipfs_encryption_key=data['cachipfs_encryption_key'],
        email=data['email'],
    )


async def api_v1_cachipfs_objects_get(
    nar_path: str,
) -> Optional[str]:
    await log('info', 'Looking up IPFS CID for %s on CachIPFS', nar_path)

    try:
        data = await api(
            headers={'authorization': config.cachipfs.API_TOKEN},
            method='GET',
            params=dict(
                nar_path=nar_path,
            ),
            path='/api/v1/cachipfs/objects'
        )
    except Error:
        return None
    else:
        return data['cid']


async def api_v1_cachipfs_objects_post(
    cid: str,
    nar_path: str,
) -> None:
    await log('info', 'Announcing to cachipfs cid: %s', cid)
    await api(
        headers={'authorization': config.cachipfs.API_TOKEN},
        method='POST',
        params=dict(
            cid=cid,
            nar_path=nar_path,
        ),
        path='/api/v1/cachipfs/objects'
    )
