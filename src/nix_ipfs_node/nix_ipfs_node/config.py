# Standard library
import os
import urllib.parse

# Constants
COORDINATOR_URL = os.environ['NIX_IPFS_COORDINATOR_URL']
PORT = os.environ['NIX_IPFS_NODE_PORT']

_SUBSTITUTER = urllib.parse.urlparse(os.environ['NIX_IPFS_NODE_SUBSTITUTER'])
SUBSTITUTER_SCHEME = _SUBSTITUTER.scheme
SUBSTITUTER_NETLOC = _SUBSTITUTER.netloc
SUBSTITUTER = f'{SUBSTITUTER_SCHEME}://{SUBSTITUTER_NETLOC}'
