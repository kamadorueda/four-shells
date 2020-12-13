# Standard library
import logging
from typing import (
    Any,
)

# Constants
LOGGER = logging.getLogger(__name__)


async def log(level: str, msg: str, *args: Any, **kwargs: Any) -> None:
    # Pending to make this non-blocking with: https://github.com/NixOS/nixpkgs/pull/103819
    getattr(LOGGER, level)(msg, *args, **kwargs)
