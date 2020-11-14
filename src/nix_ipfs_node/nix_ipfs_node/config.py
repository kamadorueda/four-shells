# Standard library
import os
import urllib.parse
from typing import (
    Dict,
)

# Third party libraries
from starlette.datastructures import (
    Headers,
)

# Environment
COORDINATOR_URL = os.environ['NIX_IPFS_NODE_COORDINATOR_URL']
DATA_DIR = os.environ['NIX_IPFS_NODE_DATA_DIR']
PORT = os.environ['NIX_IPFS_NODE_PORT']

# Constants
DATA_DIR: str = os.path.abspath(os.path.expanduser(DATA_DIR))
MAX_AGGRESSIVE_READ = 1048576  # 1 MiB

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


def patch_substituter_headers(headers: Headers) -> Dict[str, str]:
    headers_dict: Dict[str, str] = dict(headers)
    headers_dict['host'] = SUBSTITUTER_NETLOC

    return headers_dict
