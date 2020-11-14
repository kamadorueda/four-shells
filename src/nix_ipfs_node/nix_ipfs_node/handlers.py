# Third party libraries
import aiofiles
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


async def route_get(request: Request) -> Response:
    url: str = config.build_substituter_url(request.path_params['path'])
    headers = config.patch_substituter_headers(request.headers)

    async with http.request(
        headers=headers,
        method=request.method,
        url=url,
    ) as response:
        async with http.stream_response_to_tmp_file(response=response) as path:

            if url.endswith('.narinfo'):
                async with aiofiles.open(path) as handle:
                    content = await handle.read(config.MAX_FILE_READ)

                nar_info = nix_config.parse(content)

                print(nar_info)
                nar_hash = nar_info['FileHash:']



        # Pass through
        return await http.stream_from_tmp_file(path=path)


async def route_head(request: Request) -> Response:
    return await _simple_proxy_to_substituter(request)


async def route_post(request: Request) -> Response:
    return await _simple_proxy_to_substituter(request)
