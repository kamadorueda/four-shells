# Local libraries
from four_shells.cachipfs import (
    ipfs,
)


async def daemon() -> None:
    await ipfs.init()
    await ipfs.configurate()
    await ipfs.daemon()
