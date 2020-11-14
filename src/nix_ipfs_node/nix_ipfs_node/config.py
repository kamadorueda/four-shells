# Standard library
import asyncio
from contextlib import (
    asynccontextmanager,
    suppress,
)
from itertools import (
    cycle,
)
import os
import urllib.parse
from uuid import uuid4 as uuid
import shutil
from typing import (
    Dict,
    Tuple,
)

# Third party libraries
from starlette.datastructures import (
    Headers,
)

# Environment
COORDINATOR_URL = os.environ['NIX_IPFS_NODE_COORDINATOR_URL']
DATA_DIR = os.environ['NIX_IPFS_NODE_DATA_DIR']
IPFS_API_PORT = os.environ['NIX_IPFS_NODE_IPFS_API_PORT']
IPFS_GATEWAY_PORT = os.environ['NIX_IPFS_NODE_IPFS_GATEWAY_PORT']
IPFS_SWARM_PORT = os.environ['NIX_IPFS_NODE_IPFS_SWARM_PORT']
PORT = os.environ['NIX_IPFS_NODE_PORT']

# Constants
DATA_DIR: str = os.path.abspath(os.path.expanduser(DATA_DIR))
DATA_EPH: str = os.path.join(DATA_DIR, 'ephemeral')
DATA_IPFS: str = os.path.join(DATA_DIR, 'ipfs')
DATA_EPH_FILES: Dict[str, asyncio.Lock] = {
    os.path.join(DATA_EPH, str(uuid())): None for _ in range(25)
}
_DATA_EPH_FILES_ITER = cycle(DATA_EPH_FILES.items())
MAX_FILE_READ = 1048576  # 1 MiB
MAX_FILE_SIZE = 1073742000 # 1GiB

_SUBSTITUTER = urllib.parse.urlparse(os.environ['NIX_IPFS_NODE_SUBSTITUTER'])
SUBSTITUTER_SCHEME = _SUBSTITUTER.scheme
SUBSTITUTER_NETLOC = _SUBSTITUTER.netloc
SUBSTITUTER = f'{SUBSTITUTER_SCHEME}://{SUBSTITUTER_NETLOC}'


def build_coordinator_url(path: str, **kwargs: str) -> str:
    path = path.format(**{
        key: urllib.parse.quote_plus(val) for key, val in kwargs.items()
    })

    return f'{COORDINATOR_URL}/{path}'


def build_substituter_url(path: str) -> str:
    return f'{SUBSTITUTER}/{path}'


def build_ipfs_url(cid: str) -> str:
    return f'http://127.0.0.1:{IPFS_GATEWAY_PORT}/{cid}'


@asynccontextmanager
def ephemeral_file() -> Tuple[str, asyncio.Lock]:
    path, lock = next(_DATA_EPH_FILES_ITER)

    async with lock:
        yield path


def patch_substituter_headers(headers: Headers) -> Dict[str, str]:
    headers_dict: Dict[str, str] = dict(headers)
    headers_dict['host'] = SUBSTITUTER_NETLOC

    return headers_dict


def side_effects() -> None:
    os.makedirs(DATA_DIR, mode=0o700, exist_ok=True)
    with suppress(FileNotFoundError):
        shutil.rmtree(DATA_EPH)
    os.makedirs(DATA_EPH, mode=0o700)

    for eph_file in DATA_EPH_FILES:
        DATA_EPH_FILES[eph_file] = asyncio.Lock()
        eph_file_descriptor = os.open(eph_file, os.O_CREAT, 0o600)
        with open(eph_file_descriptor, 'w'):
            pass
