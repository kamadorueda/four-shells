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
AWS_CLOUDFRONT_DOMAIN: str = environ['AWS_CLOUDFRONT_DOMAIN']
PRODUCTION: bool = 'PRODUCTION' in environ
GOOGLE_OAUTH_CLIENT_ID_SERVER: str = environ['GOOGLE_OAUTH_CLIENT_ID_SERVER']
GOOGLE_OAUTH_SECRET_SERVER: str = environ['GOOGLE_OAUTH_SECRET_SERVER']
SERVER_PATH_PUBLIC: str = environ['SERVER_PATH_PUBLIC']
SESSION_SECRET: str = environ['SERVER_SESSION_SECRET']
SESSION_DURATION: int = 86400
SESSION_COOKIE: str = 'four_shells_session'

# Derived
CDN: str = 'https://' + (
    AWS_CLOUDFRONT_DOMAIN
    if PRODUCTION
    else 'localhost:8401'
)


def from_cdn(location: str) -> str:
    return CDN + location


# Templating engine
TPL = Jinja2Templates(path.join(SERVER_PATH_PUBLIC, 'templates'))
TPL.env.autoescape = False
TPL.env.globals['from_cdn'] = from_cdn
