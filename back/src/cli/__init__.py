# Standard libraries
import os

# Third party libraries
import click
from starlette.templating import Jinja2Templates
import uvicorn

# Local libraries
from config import (
    common as common_config,
    server as server_config,
)


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
    common_config.DATA = os.path.abspath(os.path.expanduser(data))
    common_config.DATA_CACHIPFS = os.path.join(common_config.DATA, 'cachipfs')
    common_config.DATA_CACHIPFS_REPO = os.path.join(common_config.DATA_CACHIPFS, 'repo')
    common_config.DATA_EPHEMERAL = os.path.join(common_config.DATA, 'ephemeral')
    common_config.DEBUG = debug

    os.makedirs(common_config.DATA, mode=0o700, exist_ok=True)
    os.makedirs(common_config.DATA_CACHIPFS, mode=0o700, exist_ok=True)
    os.makedirs(common_config.DATA_CACHIPFS_REPO, mode=0o700, exist_ok=True)
    os.makedirs(common_config.DATA_EPHEMERAL, mode=0o700, exist_ok=True)

    common_config.spawn_ephemeral_paths()


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
    default='0.0.0.0',
    help='Bind server to this host',
    required=True,
    show_default=True,
    type=str,
)
@click.option(
    '--port',
    default=8400,
    help='Bind server to this port',
    required=True,
    show_default=True,
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
    server_config.AWS_ACCESS_KEY_ID = aws_access_key_id
    server_config.AWS_CLOUDFRONT_DOMAIN = aws_cloudfront_domain
    server_config.AWS_REGION = aws_region
    server_config.AWS_SECRET_ACCESS_KEY = aws_secret_access_key
    server_config.CDN = 'https://' + (
        aws_cloudfront_domain
        if production
        else 'localhost:8401'
    )
    server_config.GOOGLE_OAUTH_CLIENT_ID = google_oauth_client_id
    server_config.GOOGLE_OAUTH_SECRET = google_oauth_secret
    server_config.PRODUCTION = production
    server_config.SESSION_SECRET = session_secret
    server_config.TPL = Jinja2Templates(
        directory=os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'templates',
        ),
    )
    server_config.TPL.env.autoescape = False
    server_config.TPL.env.globals['from_cdn'] = server_config.from_cdn

    uvicorn.run(
        app='server.asgi:APP',
        host=host,
        interface='asgi3',
        log_level='debug' if common_config.DEBUG else 'info',
        loop='uvloop',
        port=port,
        workers=1,
    )


if __name__ == '__main__':
    try:
        main(
            prog_name='4s',
        )
    finally:
        common_config.delete_ephemeral_paths()
