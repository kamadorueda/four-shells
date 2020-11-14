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
    nix_config,
)

async def on_startup() -> None:
    config.side_effects()


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


async def route_get__narinfo(
    headers: Headers,
    request: Request,
    url: str,
) -> Response:
    async with http.request(
        headers=headers,
        method=request.method,
        url=url,
    ) as response:
        content = await response.content.read(config.MAX_FILE_READ)
        nar_info = nix_config.parse_bytes(content)

        narinfo_hash = nar_info['FileHash:']
        nar_url = nar_info['URL:']

        return await _simple_proxy_to_substituter(request)


async def route_get(request: Request) -> Response:
    url: str = config.build_substituter_url(request.path_params['path'])
    headers = config.patch_substituter_headers(request.headers)

    if url.endswith('.narinfo'):
        return await route_get__narinfo(
            headers=headers,
            request=request,
            url=url,
        )

    if url.endswith('.nar.xz'):
        return await _simple_proxy_to_substituter(request)

    return await _simple_proxy_to_substituter(request)


async def route_head(request: Request) -> Response:
    return await _simple_proxy_to_substituter(request)


async def route_post(request: Request) -> Response:
    return await _simple_proxy_to_substituter(request)
