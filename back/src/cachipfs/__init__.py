# Standard library
import contextlib
from glob import (
    iglob as glob,
)
import os
from typing import (
    Tuple,
)

# Local libraries
import ipfs
from logs import (
    log,
)
import nix
import system


async def publish(nix_store_paths: Tuple[str, ...]) -> bool:
    async with system.ephemeral_dir() as directory:
        for nix_store_path in nix_store_paths:
            await log('info', 'Serializing: %s', nix_store_path)
            with contextlib.suppress(SystemError):
                await nix.copy(f'file://{directory}', nix_store_path)

        for nar_path in await system.recurse_dir(directory):
            nar_path = os.path.join(directory, nar_path)

            await ipfs.add(nar_path)
