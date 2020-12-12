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
_FORMAT: str = '[%(levelname)s] %(message)s'
_LOGGER: logging.Logger = logging.getLogger('Skims')
_LOGGER_FORMATTER: logging.Formatter = logging.Formatter(_FORMAT)
_LOGGER_HANDLER: logging.StreamHandler = logging.StreamHandler()


def configure() -> None:
    _LOGGER.setLevel(logging.INFO)
    _LOGGER.addHandler(_LOGGER_HANDLER)
    _LOGGER_HANDLER.setLevel(logging.INFO)
    _LOGGER_HANDLER.setFormatter(_LOGGER_FORMATTER)
    _LOGGER_HANDLER.setStream(sys.stdout)



def set_level(level: int) -> None:
    _LOGGER.setLevel(level)
    _LOGGER_HANDLER.setLevel(level)


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


# Side effects
configure()
