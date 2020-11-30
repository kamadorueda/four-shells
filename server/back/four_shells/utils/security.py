# Standard library
import secrets


def create_secret() -> str:
    return secrets.token_hex(16)
