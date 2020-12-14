# Standard library
from contextlib import (
    asynccontextmanager,
)
from typing import (
    Dict,
    Tuple,
)

# Local libraries
import config.cachipfs
from logs import (
    log,
)
import system


async def copy(dir: str, path: str) -> bool:
    command: Tuple[str, ...] = (
        'nix',
        'copy',
        '--to', dir,
        path,
    )

    code, out, err = await system.read(*command)

    if code != 0:
        await system.raise_from_cmd(
            code=code,
            command=command,
            err=err,
            out=out,
        )

    return code == 0
