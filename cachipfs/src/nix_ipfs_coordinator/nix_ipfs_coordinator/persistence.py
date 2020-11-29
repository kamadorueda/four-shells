# Standard library
from typing import (
    Optional,
)

# Third party libraries
import aioredis


CONNECTION: aioredis.ConnectionsPool = None


async def delete(hash: str, key: str) -> bool:
    # https://redis.io/commands/hdel
    return await CONNECTION.execute('HDEL', hash, key) == 1


async def get(hash: str, key: str) -> Optional[str]:
    # https://redis.io/commands/hget
    value: bytes = await CONNECTION.execute('HGET', hash, key)

    return value.decode() if value else None


async def set(hash: str, key: str, value: str) -> bool:
    # https://redis.io/commands/hsetnx
    return 0 <= await CONNECTION.execute('HSETNX', hash, key, value) <= 1
