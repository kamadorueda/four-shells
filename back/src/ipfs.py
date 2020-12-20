# Standard library
from contextlib import (
    asynccontextmanager,
)
from typing import (
    Dict,
    Tuple,
)

# Local libraries
import config.cachipfs
from logs import (
    log,
)
import system


def get_env() -> Dict[str, str]:
    return {
        'IPFS_PATH': config.cachipfs.IPFS_REPO,
    }


async def add(path: str) -> Tuple[bool, str]:
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
    cid = out.decode()[:-1]

    if code == 0:
        await log('info', 'IPFS added path: %s, cid: %s', path, cid)
    else:
        await system.log_error(code=code, command=command, err=err, out=out)

    return code == 0, cid


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
async def get(cid: str, *, timeout: str = '60s') -> Tuple[bool, str]:
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
            await system.log_error(code=code, command=command, err=err, out=out)

        yield code == 0, path
