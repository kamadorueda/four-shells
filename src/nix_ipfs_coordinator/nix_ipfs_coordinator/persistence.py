# Third party libraries
import aioredis


CONNECTION: aioredis.ConnectionsPool = None


async def delete(key: str) -> bool:
    success: bool = await CONNECTION.execute('DELETE', key) == 1
    return success


async def get(key: str) -> str:
    return await CONNECTION.execute('GET', key)


async def set(key: str, value: str) -> bool:
    success: bool = await CONNECTION.execute('SET', key, value) == "OK"
    return success
