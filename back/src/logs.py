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
_LOGGER: logging.Logger = logging.getLogger('4s')


def blocking_log(level: str, msg: str, *args: Any, **kwargs: Any) -> None:
    if not _LOGGER.hasHandlers():
        _LOGGER.addHandler(logging.StreamHandler())
        _LOGGER.setLevel(logging.INFO)

        _LOGGER.handlers[0].setFormatter(
            logging.Formatter('[%(levelname)s] %(message)s'),
        )
        _LOGGER.handlers[0].setLevel(logging.INFO)
        _LOGGER.handlers[0].setStream(sys.stdout)

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
