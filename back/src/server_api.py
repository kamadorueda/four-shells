# Standard library
from aioextensions import (
    rate_limited,
)
# Third party libraries
import aiohttp
# Local libraries
from logs import (
    log,
)
from typing import (
    Any,
    Dict,
    NamedTuple,
    Optional,
)

# Constants
ENDPOINT: str = "https://4shells.com"
# ENDPOINT: str = 'http://localhost:8400'


class Error(Exception):
    pass


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
            url=f"{ENDPOINT}{path}",
        ) as response:
            try:
                data = await response.json()
            except aiohttp.ClientError:
                await log("error", "4shells API: %s", await response.text())
                data = {}

            if "error" in data:
                await log("error", "%s", data["error"])
                raise Error(data["error"])

            return data
