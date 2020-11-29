# Standard library
from typing import (
    Dict,
    Tuple,
)


def parse(content: str) -> Dict[str, Tuple[str, ...]]:
    parsed: Dict[str, Tuple[str, ...]] = {}

    for line in content.splitlines():
        line = line.strip()

        if line:
            key, values_str = line.split(' ', maxsplit=1)

            parsed[key] = tuple(values_str.split(' '))

    return parsed


def parse_bytes(content: bytes) -> Dict[str, Tuple[str, ...]]:
    return parse(content.decode())
