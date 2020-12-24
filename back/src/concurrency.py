# Standard library
from asyncio import (
    Lock,
)
import functools
from typing import (
    Any,
    Callable,
    cast,
    TypeVar,
)

# Constants
TFun = TypeVar('TFun', bound=Callable[..., Any])


def never_concurrent(function: TFun) -> TFun:
    lock = None

    @functools.wraps(function)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        nonlocal lock
        if lock is None:
            lock = Lock()

        async with lock:
            return await function(*args, **kwargs)

    return cast(TFun, wrapper)
