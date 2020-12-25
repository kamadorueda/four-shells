# Standard library
import logging
import sys
from typing import (
    Any,
)

# Third party libraries
from aioextensions import (
    in_thread,
)

# Private constants
_DEFAULT_HANDLER: logging.StreamHandler = logging.StreamHandler(sys.stdout)
_DEFAULT_HANDLER.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
_DEFAULT_HANDLER.setLevel(logging.INFO)
_LOGGER: logging.Logger = logging.getLogger()


def blocking_log(level: str, msg: str, *args: Any, **kwargs: Any) -> None:
    if 'uvicorn.asgi' in logging.Logger.manager.loggerDict:
        _LOGGER.removeHandler(_DEFAULT_HANDLER)
    else:
        _LOGGER.addHandler(_DEFAULT_HANDLER)
        _LOGGER.setLevel(logging.INFO)

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
