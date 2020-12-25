# Standard library
import os
import re
import sys
from typing import (
    Iterator,
    Tuple,
)

# Third party libraries
from aioextensions import (
    collect,
)
from logs import (
    log,
)
from starlette.requests import (
    Request,
)
from starlette.responses import (
    FileResponse,
    Response,
)
from starlette.routing import (
    Route,
    Router,
)

# Local libraries
import ipfs
import nix
import server_api
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

        # Announce to coordinator
        await collect(tuple(
            server_api.api_v1_cachipfs_objects_post(cid, f'/{nar_path}')
            for cid, nar_path in zip(
                (cid for _, cid in results),
                (os.path.relpath(nar_path, directory) for nar_path in nar_paths),
            )
        ))

    return True


async def publish(nix_store_paths: Tuple[str, ...]) -> bool:
    return all(await collect(tuple(map(publish_one, nix_store_paths))))


async def publish_from_stdin() -> bool:
    pattern = re.compile(br'(/nix/store/[\w]{32}-.*?)')

    def search_nix_store_paths_on_stdin() -> Iterator[str]:
        for line in sys.stdin.buffer:
            if match := pattern.search(line):
                nix_store_path: str = match.groups(1).decode('utf-8')
                if not nix_store_path.endswith('.drv'):
                    yield nix_store_path

    return all(await collect(map(
        publish_one,
        search_nix_store_paths_on_stdin(),
    )))


async def daemon_handle_request(request: Request) -> None:
    nar_path: str = request.url.path

    if cid := await server_api.api_v1_cachipfs_objects_get(nar_path):
        if await ipfs.is_available(cid):
            async with ipfs.get(cid) as (success, nar_path_file):
                if success:
                    return FileResponse(nar_path_file)
                else:
                    await log('info', 'CID not available on IPFS at the moment: %s', cid)
                    return Response(status_code=404)
        else:
            await log('info', 'CID not available on IPFS at the moment: %s', cid)
            return Response(status_code=404)
    else:
        await log('info', 'Nar path has not been published to CachIPFS: %s', nar_path)
        return Response(status_code=404)


DAEMON = Router(
    routes=[
        Route(
            path='/{path:path}',
            endpoint=daemon_handle_request,
            methods=['HEAD', 'GET'],
        ),
    ],
)
