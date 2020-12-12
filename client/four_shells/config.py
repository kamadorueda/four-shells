# Standard library
from asyncio import (
    Lock,
)
from itertools import (
    cycle,
)
import os
from typing import (
    Iterator,
    Tuple,
)
from uuid import (
    uuid4 as uuid,
)

# Constants
COORDINATOR_URL: str = 'https://4shells.com'
MAX_FILE_READ: int = 1_048_576  # 1 MiB
MAX_FILE_SIZE: int = 1_073_742_000  # 1GiB

# User defined
CACHIPFS_API_PORT: int = 0
CACHIPFS_GATEWAY_PORT: int = 0
CACHIPFS_NODE_PORT: int = 0
CACHIPFS_SWARM_PORT: int = 0
DATA: str = ''
DATA_CACHIPFS: str = ''
DATA_CACHIPFS_REPO: str = ''
DATA_EPHEMERAL: str = ''
DATA_EPHEMERAL_FILES_ITER: Iterator[Tuple[str, Lock]]
DEBUG: bool = False


def spawn_ephemeral_files() -> None:
    global DATA_EPHEMERAL_FILES_ITER

    DATA_EPHEMERAL_FILES_ITER = cycle([
        (os.path.join(DATA_EPHEMERAL, uuid().hex), Lock())
        for _ in range(32)
    ])
