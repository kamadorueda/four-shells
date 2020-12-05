# Standard library
import json
from os import (
    environ,
    path,
)
from starlette.requests import (
    Request,
)
from typing import (
    Dict,
)

# Third party library
from starlette.templating import (
    Jinja2Templates,
)

# Constants
AWS_ACCESS_KEY_ID_SERVER: str = environ['AWS_ACCESS_KEY_ID_SERVER']
AWS_CLOUDFRONT_DOMAIN: str = environ['AWS_CLOUDFRONT_DOMAIN']
AWS_REGION: str = environ['AWS_REGION']
AWS_SECRET_ACCESS_KEY_SERVER: str = environ['AWS_SECRET_ACCESS_KEY_SERVER']
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


def get_globals(request: Request) -> Dict[str, str]:
    return json.dumps({
        'session': request.session,
    })


# Templating engine
TPL = Jinja2Templates(path.join(SERVER_PATH_PUBLIC, 'templates'))
TPL.env.autoescape = False
TPL.env.globals['from_cdn'] = from_cdn
