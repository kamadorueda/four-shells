# Standard library
from uuid import (
    uuid4 as uuid,
)


def get_identifier() -> str:
    return uuid().hex
