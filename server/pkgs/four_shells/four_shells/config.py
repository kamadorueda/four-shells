# Standard library
from os import (
    environ,
    path,
)
import secrets

# Third party library
from starlette.templating import (
    Jinja2Templates,
)

# Constants
PRODUCTION: bool = 'PRODUCTION' in environ
GOOGLE_OAUTH_CLIENT_ID_SERVER: str = environ['GOOGLE_OAUTH_CLIENT_ID_SERVER']
GOOGLE_OAUTH_SECRET_SERVER: str = environ['GOOGLE_OAUTH_SECRET_SERVER']
SERVER_PATH_PUBLIC: str = environ['SERVER_PATH_PUBLIC']
SERVER_STATE_COOKIE_SECRET: str = secrets.token_hex(64)

# Derived
CDN: str = (
    'https://raw.githubusercontent.com/kamadorueda/four-shells/main/server/public'
    if PRODUCTION
    else 'https://localhost:8401'
)


def from_cdn(location: str) -> str:
    return CDN + location


# Templating engine
TPL = Jinja2Templates(directory=path.join(SERVER_PATH_PUBLIC, 'templates'))
TPL.env.globals['from_cdn'] = from_cdn
