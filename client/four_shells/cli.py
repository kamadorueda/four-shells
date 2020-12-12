# Standard libraries
import os

# Third party libraries
import click
import uvicorn

# Local libraries
from four_shells import (
    config,
)


@click.group(
    help=(
        'The 4s Comand Line Interface is a unified tool to manage your '
        'Four Shells services'
    ),
)
@click.option(
    '--debug',
    is_flag=True,
)
@click.option(
    '--data-dir',
    default='~/.four-shells',
    type=str,
)
def main(
    *,
    data_dir: str,
    debug: bool,
) -> None:
    config.DATA = os.path.abspath(os.path.expanduser(data_dir))
    config.DATA_CACHIPFS = os.path.join(config.DATA, 'cachipfs')
    config.DATA_CACHIPFS_REPO = os.path.join(config.DATA_CACHIPFS, 'repo')
    config.DATA_EPHEMERAL = os.path.join(config.DATA, 'ephemeral')
    config.DEBUG = debug

    os.makedirs(config.DATA, mode=0o700, exist_ok=True)
    os.makedirs(config.DATA_CACHIPFS, mode=0o700, exist_ok=True)
    os.makedirs(config.DATA_CACHIPFS_REPO, mode=0o700, exist_ok=True)
    os.makedirs(config.DATA_EPHEMERAL, mode=0o700, exist_ok=True)


@main.group(
    name='cachipfs',
)
@click.option(
    '--cachipfs-api-port',
    default=8888,
    type=int,
)
@click.option(
    '--cachipfs-gateway-port',
    default=8889,
    type=int,
)
@click.option(
    '--cachipfs-node-port',
    default=8890,
    type=int,
)
@click.option(
    '--cachipfs-swarm-port',
    default=8891,
    type=int,
)
def main_cachipfs(
    *,
    cachipfs_api_port: int,
    cachipfs_gateway_port: int,
    cachipfs_node_port: int,
    cachipfs_swarm_port: int,
) -> None:
    config.CACHIPFS_API_PORT = cachipfs_api_port
    config.CACHIPFS_GATEWAY_PORT = cachipfs_gateway_port
    config.CACHIPFS_NODE_PORT = cachipfs_node_port
    config.CACHIPFS_SWARM_PORT = cachipfs_swarm_port


@main_cachipfs.command(
    name='daemon',
)
def main_cachipfs_daemon(
) -> None:
    uvicorn.run(
        app='four_shells.cachipfs:APP',
        host='127.0.0.1',
        log_level='debug' if config.DEBUG else 'info',
        loop='uvloop',
        port=config.CACHIPFS_NODE_PORT,
        workers=1,
    )


if __name__ == '__main__':
    main(prog_name='4s')
