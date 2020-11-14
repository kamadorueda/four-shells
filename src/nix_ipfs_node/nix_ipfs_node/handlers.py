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

async def on_startup() -> None:
    config.side_effects()
    await ipfs.init()
    await ipfs.configurate()
    await ipfs.daemon()


async def on_shutdown() -> None:
    pass


async def _simple_proxy_to_substituter(request: Request) -> Response:
    url: str = config.build_substituter_url(request.path_params['path'])
    headers = config.patch_substituter_headers(request.headers)

    return await http.stream_from_substituter(
        headers=headers,
        method=request.method,
        url=url,
    )


async def route_get__nar_info(
    headers: Headers,
    request: Request,
) -> Response:
    # Check the upstream substituter .narinfo
    async with http.request(
        headers=headers,
        method=request.method,
        url=config.build_substituter_url(request.path_params['path']),
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

    return await _simple_proxy_to_substituter(request)


async def route_get__nar_xz(
    headers: Headers,
    request: Request,
) -> Response:
    return await _simple_proxy_to_substituter(request)


async def route_get(request: Request) -> Response:
    path: str = request.path_params['path']
    headers = config.patch_substituter_headers(request.headers)

    if path.endswith('.narinfo'):
        return await route_get__nar_info(
            headers=headers,
            request=request,
        )
    if path.endswith('.nar.xz'):
        return await route_get__nar_xz(
            headers=headers,
            request=request,
        )

    return await _simple_proxy_to_substituter(request)


async def route_head(request: Request) -> Response:
    return await _simple_proxy_to_substituter(request)


async def route_post(request: Request) -> Response:
    return await _simple_proxy_to_substituter(request)
