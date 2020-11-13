# Standard library
from typing import (
    Optional,
)

# Third party libraries
import aioredis


CONNECTION: aioredis.ConnectionsPool = None


async def delete(key: str) -> bool:
    return await CONNECTION.execute('DEL', key) == 1


async def get(key: str) -> Optional[str]:
    value: bytes = await CONNECTION.execute('GET', key)

    return value.decode() if value else None


async def set(key: str, value: str) -> bool:
    return await CONNECTION.execute('SET', key, value) == b'OK'
