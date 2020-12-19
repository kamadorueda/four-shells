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


async def publish_one_add_to_ipfs(path: str) -> bool:
    success, _ = await ipfs.add(path)
    return success


async def publish_one_serialize_nix_store_path(
    directory: str,
    nix_store_path: str,
) -> bool:
    success = await nix.copy(f'file://{directory}', nix_store_path)
    return success


async def publish_one(nix_store_path: str) -> bool:
    async with system.ephemeral_dir() as directory:
        return await publish_one_serialize_nix_store_path(
            directory,
            nix_store_path,
        ) and await collect(tuple(
            publish_one_add_to_ipfs(os.path.join(directory, nar_path))
            for nar_path in await system.recurse_dir(directory)
        ))


async def publish(nix_store_paths: Tuple[str, ...]) -> bool:
    return all(await collect(tuple(map(publish_one, nix_store_paths))))
