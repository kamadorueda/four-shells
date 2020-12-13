# Standard library
from asyncio import (
    Lock,
)
import contextlib
from itertools import (
    cycle,
)
import os
import shutil
from typing import (
    Iterator,
    Tuple,
)
from uuid import (
    uuid4 as uuid,
)

# Constants
MAX_FILE_READ: int = 1_048_576  # 1 MiB
MAX_FILE_SIZE: int = 1_073_742_000  # 1GiB

# User defined
DATA: str
DATA_CACHIPFS: str
DATA_CACHIPFS_REPO: str
DATA_EPHEMERAL: str
DATA_EPHEMERAL_DIRS_ITER: Iterator[Tuple[str, Lock]]
DATA_EPHEMERAL_FILES_ITER: Iterator[Tuple[str, Lock]]
DEBUG: bool = False


def spawn_ephemeral_paths() -> None:
    global DATA_EPHEMERAL_DIRS_ITER
    global DATA_EPHEMERAL_FILES_ITER

    DATA_EPHEMERAL_DIRS_ITER = cycle([
        (os.path.join(DATA_EPHEMERAL, uuid().hex), Lock())
        for _ in range(32)
    ])
    DATA_EPHEMERAL_FILES_ITER = cycle([
        (os.path.join(DATA_EPHEMERAL, uuid().hex), Lock())
        for _ in range(32)
    ])


def delete_ephemeral_paths() -> None:
    with contextlib.suppress(NameError):
        shutil.rmtree(DATA_EPHEMERAL)
