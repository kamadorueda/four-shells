# Standard libraries
from datetime import (
    datetime,
)
from typing import (
    Any,
)


def json_cast(obj: Any) -> Any:
    if isinstance(obj, set):
        obj = list(obj)
    elif isinstance(obj, dict):
        obj = dict(zip(obj, map(json_cast, obj.values())))

    return obj


def get_ttl(seconds: int) -> int:
    return int(datetime.now().timestamp()) + seconds
