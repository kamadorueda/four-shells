# Third party libraries
from starlette.applications import (
    Starlette,
)

# Local libraries
from four_shells.cachipfs import (
    ipfs,
)


async def on_startup() -> None:
    await ipfs.init()
    await ipfs.configurate()
    await ipfs.daemon()


# Constats
APP = Starlette(
    on_startup=[
        on_startup,
    ],
    routes=[
    ],
)
