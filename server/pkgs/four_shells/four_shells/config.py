# Standard library
from os import (
    environ,
)
import secrets

# Constants
GOOGLE_OAUTH_CLIENT_ID_SERVER: str = environ['GOOGLE_OAUTH_CLIENT_ID_SERVER']
GOOGLE_OAUTH_SECRET_SERVER: str = environ['GOOGLE_OAUTH_SECRET_SERVER']
SERVER_STATE_COOKIE_SECRET: str = secrets.token_hex(64)
PRODUCTION: bool = 'PRODUCTION' in environ
