# Standard library
import os
from typing import (
    Tuple,
)

# Third party libraries
from aioextensions import (
    collect,
)

# Local libraries
import ipfs
import nix
import system


async def publish_one(nix_store_path: str) -> bool:
    async with system.ephemeral_dir() as directory:
        # Serialize the nix_store_path into NAR formatted paths
        if not await nix.copy(f'file://{directory}', nix_store_path):
            return False

        # Absolute NAR formatted paths
        nar_paths = tuple(
            nar_path
            for nar_path in await system.recurse_dir(directory)
            if os.path.basename(nar_path) not in {'nix-cache-info'}
        )

        # Tuple[success, cid]
        results = await collect(tuple(map(ipfs.add, nar_paths)))

        # Check all files were added to IPFS successfully
        if not all(success for success, _ in results):
            return False

        for cid, nar_path in zip(
            (cid for _, cid in results),
            (os.path.relpath(nar_path, directory) for nar_path in nar_paths),
        ):
            # Announce to coordinator
            pass

    return True


async def publish(nix_store_paths: Tuple[str, ...]) -> bool:
    return all(await collect(tuple(map(publish_one, nix_store_paths))))
