# Standard library
import asyncio
from contextlib import (
    asynccontextmanager,
)
import json
from typing import (
    Dict,
    Tuple,
)

# Third party libraries
from aioextensions import (
    collect,
)

# Local libraries
from four_shells import (
    config,
    system,
)
from four_shells.logs import (
    log,
)


def get_env() -> Dict[str, str]:
    return {
        'IPFS_PATH': config.DATA_CACHIPFS_REPO,
    }


async def _raise(
    code: int,
    command: Tuple[str, ...],
    err: bytes,
    out: bytes,
) -> None:
    await log(
        'error',
        'Command: %s\n'
        'Exit code: %s\n'
        'Stdout: %s\n'
        'Stderr: %s\n',
        command,
        code,
        out.decode(),
        err.decode(),
    )

    raise SystemError()


async def init() -> None:
    command: Tuple[str, ...] = (
        'ipfs',
        'init',
        '--algorithm', 'ed25519',
        '--empty-repo',
    )

    code, out, err = await system.read(*command, env=get_env())

    if code == 0:
        await log(
            'info',
            'IPFS repository correctly initialized at: %s',
            config.DATA_CACHIPFS_REPO,
        )
    elif b'ipfs configuration file already exists' in err:
        await log(
            'info',
            'IPFS repository already exists at: %s, reusing it',
            config.DATA_CACHIPFS_REPO,
        )
    else:
        await _raise(code=code, command=command, err=err, out=out)


async def configurate() -> None:
    command: Tuple[str, ...] = (
        'ipfs',
        'config',
        '--json',
        'Addresses',
        json.dumps({
            'API': f'/ip4/127.0.0.1/tcp/{config.CACHIPFS_API_PORT}',
            'Announce': [],
            'Gateway': F'/ip4/127.0.0.1/tcp/{config.CACHIPFS_GATEWAY_PORT}',
            'NoAnnounce': [],
            'Swarm': [
                f'/ip4/0.0.0.0/tcp/{config.CACHIPFS_SWARM_PORT}',
                f'/ip6/::/tcp/{config.CACHIPFS_SWARM_PORT}',
                f'/ip4/0.0.0.0/udp/{config.CACHIPFS_SWARM_PORT}/quic',
                f'/ip6/::/udp/{config.CACHIPFS_SWARM_PORT}/quic'
            ]
        })
    )

    code, out, err = await system.read(*command, env=get_env())

    if code == 0:
        await log('info', 'IPFS repository correctly configured')
    else:
        await _raise(code=code, command=command, err=err, out=out)


async def daemon() -> None:
    command: Tuple[str, ...] = ('ipfs', 'daemon')

    await log('info', 'IPFS Daemon starting')

    process = await system.call(*command, env=get_env())

    async def daemon_stdout():
        while True:
            if out := await process.stdout.readline():
                await log('info', 'IPFS Daemon stdout: %s', out[:-1].decode())
            else:
                break

    async def daemon_stderr():
        while True:
            if err := await process.stderr.readline():
                await log('error', 'IPFS Daemon stdout: %s', err[:-1].decode())
            else:
                break

    await collect((
        daemon_stdout(),
        daemon_stderr(),
    ))


async def add(path: str) -> str:
    command: Tuple[str, ...] = (
        'ipfs',
        'add',
        '--chunker', 'size-1024',
        '--hash', 'sha2-256',
        '--quieter',
        '--pin',
        path,
    )

    code, out, err = await system.read(*command, env=get_env())
    cid = out.decode()

    if code == 0:
        await log('info', 'IPFS added cid: %s', cid)
    else:
        await _raise(code=code, command=command, err=err, out=out)

    return cid


async def is_available(cid: str, *, timeout: str = '5s') -> bool:
    command: Tuple[str, ...] = (
        'ipfs',
        '--timeout', timeout,
        'cat',
        '--length', '1',
        cid,
    )

    code, *_ = await system.read(*command, env=get_env())

    return code == 0


@asynccontextmanager
async def get(cid: str, *, timeout: str = '60s') -> str:
    async with config.ephemeral_file() as path:
        command: Tuple[str, ...] = (
            'ipfs',
            '--timeout', timeout,
            'get',
            '--output', path,
            cid,
        )

        code, out, err = await system.read(*command, env=get_env())

        if code == 0:
            await log('info', 'IPFS got cid: %s', cid)
        else:
            await _raise(code=code, command=command, err=err, out=out)

        yield path
