# Standard library
from typing import (
    Tuple,
)

# Local libraries
from logs import (
    log,
)
import system


async def copy(dir: str, path: str) -> bool:
    command: Tuple[str, ...] = (
        'nix',
        '--print-build-logs',
        '--verbose',
        'copy',
        '--no-check-sigs',
        '--to', dir,
        path,
    )

    code, *_ = await system.read(*command, stderr=None, stdout=None)

    if code == 0:
        await log('info', 'Nix copied: %s, to %s', path, dir)
    else:
        await system.log_error(code=code, command=command)

    return code == 0
