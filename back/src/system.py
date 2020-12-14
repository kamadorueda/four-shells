# Standard library
import aiofiles
import asyncio
from contextlib import (
    asynccontextmanager,
)
import os
import shutil
from typing import (
    Any,
    Dict,
    Optional,
    Tuple,
)

# Third party libraries
from aioextensions import (
    in_thread,
)

# Local libraries
import config.common


async def call(
    binary: str,
    *binary_args: str,
    cwd: Optional[str] = None,
    env: Optional[Dict[str, str]] = None,
    stdin: int = asyncio.subprocess.DEVNULL,
    stdout: int = asyncio.subprocess.PIPE,
    stderr: int = asyncio.subprocess.PIPE,
    **kwargs: Any,
) -> asyncio.subprocess.Process:
    process = await asyncio.create_subprocess_exec(
        binary,
        *binary_args,
        cwd=cwd,
        env={
            **os.environ.copy(),
            **(env or {}),
        },
        stderr=stderr,
        stdin=stdin,
        stdout=stdout,
        **kwargs,
    )

    return process


@asynccontextmanager
async def ephemeral_file() -> str:
    path, lock = next(config.common.DATA_EPHEMERAL_FILES_ITER)

    async with lock:
        async with aiofiles.open(path, 'w'):
            pass

        yield path


@asynccontextmanager
async def ephemeral_dir() -> str:
    path, lock = next(config.common.DATA_EPHEMERAL_DIRS_ITER)

    async with lock:
        await in_thread(shutil.rmtree(path, ignore_errors=True))

        yield path


async def read(
    binary: str,
    *binary_args: str,
    cwd: Optional[str] = None,
    env: Optional[Dict[str, str]] = None,
    stdin_bytes: Optional[bytes] = None,
    stdout: int = asyncio.subprocess.PIPE,
    stderr: int = asyncio.subprocess.PIPE,
    **kwargs: Any,
) -> Tuple[int, bytes, bytes]:
    process: asyncio.subprocess.Process = await call(
        binary,
        *binary_args,
        cwd=cwd,
        env=env,
        stdin=(
            asyncio.subprocess.DEVNULL
            if stdin_bytes is None
            else asyncio.subprocess.PIPE
        ),
        stdout=stdout,
        stderr=stderr,
        **kwargs,
    )

    out, err = await process.communicate(input=stdin_bytes)
    code = -1 if process.returncode is None else process.returncode

    return code, out, err
