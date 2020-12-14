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
import system
from logs import (
    log,
)
import nix


async def publish(nix_store_paths: Tuple[str, ...]) -> bool:
    async with system.ephemeral_dir() as directory:
        for nix_store_path in nix_store_paths:
            await log('info', 'Serializing: %s', nix_store_path)
            with contextlib.suppress(SystemError):
                await nix.copy(f'file://{directory}', nix_store_path)

        for nar_path in os.listdir(directory):
            nar_path = os.path.join(directory, nar_path)

            await log('info', 'Nar: %s', nar_path)
