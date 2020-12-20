# Standard libraries
import os
from typing import (
    Tuple,
)

# Third party libraries
from aioextensions import (
    run,
)
import click
from logs import blocking_log
from starlette.templating import (
    Jinja2Templates,
)
import uvicorn

# Local libraries
import cachipfs
import config.cachipfs
import config.common
import config.server
import server_api


@click.group(
    help=(
        'The 4s Comand Line Interface is a unified tool to manage your '
        'Four Shells services'
    ),
)
@click.option(
    '--data',
    default='~/.four-shells',
    help='State directory',
    show_default=True,
    type=str,
)
@click.option(
    '--debug',
    help='Enable debug mode',
    is_flag=True,
)
def main(
    *,
    data: str,
    debug: bool,
) -> None:
    main_config(
        data=data,
        debug=debug,
    )


def main_config(
    *,
    data: str,
    debug: bool,
) -> None:
    config.common.DATA = os.path.abspath(os.path.expanduser(data))
    config.common.DATA_CACHIPFS = os.path.join(config.common.DATA, 'cachipfs')
    config.common.DATA_CACHIPFS_REPO = os.path.join(config.common.DATA_CACHIPFS, 'repo')
    config.common.DATA_EPHEMERAL = os.path.join(config.common.DATA, 'ephemeral')
    config.common.DEBUG = debug

    os.makedirs(config.common.DATA, mode=0o700, exist_ok=True)
    os.makedirs(config.common.DATA_CACHIPFS, mode=0o700, exist_ok=True)
    os.makedirs(config.common.DATA_CACHIPFS_REPO, mode=0o700, exist_ok=True)
    os.makedirs(config.common.DATA_EPHEMERAL, mode=0o700, exist_ok=True)

    config.common.spawn_ephemeral_paths()


@main.group(
    name='cachipfs',
)
@click.option(
    '--api-token',
    help='You API token, grab yours at https://4shells.com/cachipfs',
    required=True,
    type=str,
)
@click.option(
    '--ipfs-repo',
    default='~/.ipfs',
    help='IPFS repository path',
    show_default=True,
    type=str,
)
def main_cachipfs(
    *,
    api_token: str,
    ipfs_repo: str,
) -> None:
    main_cachipfs_config(
        api_token=api_token,
        ipfs_repo=ipfs_repo,
    )


def main_cachipfs_config(
    *,
    api_token: str,
    ipfs_repo: str,
) -> None:
    config.cachipfs.API_TOKEN = api_token
    data = run(server_api.api_v1_cachipfs_config_get())
    blocking_log('info', 'Welcome %s!', data.email)
    config.cachipfs.ENCRYPTION_KEY = data.cachipfs_encryption_key
    config.cachipfs.IPFS_REPO = ipfs_repo


@main_cachipfs.command(
    name='publish',
    help='Publish Nix-store paths to CachIPFS',
)
@click.argument(
    'nix_store_paths',
    metavar='NIX_STORE_PATH',
    nargs=-1,
    type=str,
)
def main_cachipfs_publish(
    *,
    nix_store_paths: Tuple[str, ...],
) -> None:
    run(cachipfs.publish(nix_store_paths))


@main.command(
    name='server',
)
@click.option(
    '--aws-access-key-id',
    required=True,
    type=str,
)
@click.option(
    '--aws-cloudfront-domain',
    required=True,
    type=str,
)
@click.option(
    '--aws-region',
    required=True,
    type=str,
)
@click.option(
    '--aws-secret-access-key',
    required=True,
    type=str,
)
@click.option(
    '--google-oauth-client-id',
    required=True,
    type=str,
)
@click.option(
    '--google-oauth-secret',
    required=True,
    type=str,
)
@click.option(
    '--host',
    help='Bind server to this host',
    required=True,
    type=str,
)
@click.option(
    '--port',
    help='Bind server to this port',
    required=True,
    type=int,
)
@click.option(
    '--production',
    is_flag=True,
)
@click.option(
    '--session-secret',
    required=True,
    type=str,
)
def main_server(
    *,
    aws_access_key_id: str,
    aws_cloudfront_domain: str,
    aws_region: str,
    aws_secret_access_key: str,
    host: str,
    port: str,
    production: bool,
    google_oauth_client_id: str,
    google_oauth_secret: str,
    session_secret: str,
) -> None:
    main_server_config(
        aws_access_key_id=aws_access_key_id,
        aws_cloudfront_domain=aws_cloudfront_domain,
        aws_region=aws_region,
        aws_secret_access_key=aws_secret_access_key,
        production=production,
        google_oauth_client_id=google_oauth_client_id,
        google_oauth_secret=google_oauth_secret,
        session_secret=session_secret,
    )

    uvicorn.run(
        app='server.asgi:APP',
        host=host,
        interface='asgi3',
        log_level='debug' if config.common.DEBUG else 'info',
        loop='uvloop',
        port=port,
        workers=1,
    )


def main_server_config(
    *,
    aws_access_key_id: str,
    aws_cloudfront_domain: str,
    aws_region: str,
    aws_secret_access_key: str,
    production: bool,
    google_oauth_client_id: str,
    google_oauth_secret: str,
    session_secret: str,
) -> None:
    config.server.AWS_ACCESS_KEY_ID = aws_access_key_id
    config.server.AWS_CLOUDFRONT_DOMAIN = aws_cloudfront_domain
    config.server.AWS_REGION = aws_region
    config.server.AWS_SECRET_ACCESS_KEY = aws_secret_access_key
    config.server.CDN = 'https://' + (
        aws_cloudfront_domain
        if production
        else 'localhost:8401'
    )
    config.server.GOOGLE_OAUTH_CLIENT_ID = google_oauth_client_id
    config.server.GOOGLE_OAUTH_SECRET = google_oauth_secret
    config.server.PRODUCTION = production
    config.server.SESSION_SECRET = session_secret
    config.server.TPL = Jinja2Templates(
        directory=os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'templates',
        ),
    )
    config.server.TPL.env.autoescape = False
    config.server.TPL.env.globals['from_cdn'] = config.server.from_cdn


if __name__ == '__main__':
    try:
        main(
            prog_name='4s',
        )
    finally:
        config.common.delete_ephemeral_paths()
