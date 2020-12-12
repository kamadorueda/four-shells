# Standard library
import logging
from typing import (
    Any,
)

# Third party libraries
from aioextensions import (
    in_thread,
)

# Private constants
_LOGGER: logging.Logger = logging.getLogger('Skims')


def blocking_log(level: str, msg: str, *args: Any, **kwargs: Any) -> None:
    getattr(_LOGGER, level)(msg, *args, **kwargs)


async def log(level: str, msg: str, *args: Any, **kwargs: Any) -> None:
    await in_thread(blocking_log, level, msg, *args, **kwargs)


def blocking_log_exception(
    level: str,
    exception: BaseException,
    **meta_data: str,
) -> None:
    exc_type: str = type(exception).__name__
    exc_msg: str = str(exception)
    blocking_log(level, 'Exception: %s, %s, %s', exc_type, exc_msg, meta_data)


async def log_exception(
    level: str,
    exception: BaseException,
    **meta_data: str,
) -> None:
    await in_thread(blocking_log_exception, level, exception, **meta_data)
