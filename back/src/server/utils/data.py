# Standard libraries
from typing import (
    Any,
)


def json_cast(obj: Any) -> Any:
    if isinstance(obj, set):
        obj = list(obj)
    elif isinstance(obj, dict):
        obj = dict(zip(obj, map(json_cast, obj.values())))

    return obj
