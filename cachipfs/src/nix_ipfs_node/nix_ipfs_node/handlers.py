# Third party libraries
import aiofiles
from starlette.datastructures import (
    Headers,
)
from starlette.requests import (
    Request,
)
from starlette.responses import (
    Response,
)

# Local libraries
from nix_ipfs_node import (
    config,
    http,
    ipfs,
    nix_config,
)
from nix_ipfs_node.log import (
    log,
)


async def on_startup() -> None:
    config.side_effects()
    await ipfs.init()
    await ipfs.configurate()
    await ipfs.daemon()


async def on_shutdown() -> None:
    pass


async def proxy_to_substituter(request: Request) -> Response:
    return await http.stream_from_substituter(
        headers=config.patch_substituter_headers(request.headers),
        method=request.method,
        url=config.build_substituter_url(request.url.path[1:]),
    )


async def proxy_as_narinfo(request: Request) -> Response:
    drv_hash: str = request.path_params['drv_hash']
    headers = config.patch_substituter_headers(request.headers)

    # Check the upstream substituter .narinfo
    async with http.request(
        headers=headers,
        method=request.method,
        url=config.build_substituter_url(f'{drv_hash}.narinfo'),
    ) as response:
        nar_info_content = await response.content.read(config.MAX_FILE_READ)

    # Inspect the .narinfo
    nar_info = nix_config.parse_bytes(nar_info_content)
    nar_xz_hash = nar_info['FileHash:'][0]
    nar_xz_url = nar_info['URL:'][0]

    # Check if this nar_xz_hash has a translation
    if nar_xz_cid := await http.coordinator_get(nar_xz_hash):
        # Translation exists
        pass
    else:
        # Translation does not exist
        # Download the .nar.xz and add it to ipfs
        async with http.request(
            headers=headers,
            method=request.method,
            url=config.build_substituter_url(nar_xz_url),
        ) as response:
            async with http.stream_response_to_tmp_file(
                response=response,
            ) as path:
                nar_xz_cid = await ipfs.add(path)

        # Announce the nar_xz_cid to the coordinator
        await http.coordinator_post(nar_xz_hash, nar_xz_cid)

    return await proxy_to_substituter(request)


async def proxy_as_nar_xz(request: Request) -> Response:
    nar_xz_hash: str = request.path_params['nar_xz_hash']
    nar_xz_hash = f'sha256:{nar_xz_hash}'

    # Check if it's available on IPFS
    if nar_xz_cid := await http.coordinator_get(nar_xz_hash):
        await log('info', 'nar_xz_hash: %s, is on coordinator', nar_xz_hash)
        if await ipfs.is_available(nar_xz_cid):
            await log('info', 'nar_xz_cid: %s, is on IPFS, streaming', nar_xz_cid)
            async with ipfs.get(nar_xz_cid) as path:
                return await http.stream_from_tmp_file(path=path)
        else:
            await log('info', 'nar_xz_cid: %s, is on IPFS', nar_xz_cid)
    else:
        await log('info', 'nar_xz_hash: %s, is not on coordinator', nar_xz_hash)

    return await proxy_to_substituter(request)
