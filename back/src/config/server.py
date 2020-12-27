# Standard library
import json
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
SESSION_DURATION: int = 86400
SESSION_COOKIE: str = 'four_shells_session'

# User defined
AWS_ACCESS_KEY_ID: str
AWS_CLOUDFRONT_DOMAIN: str
AWS_REGION: str
AWS_SECRET_ACCESS_KEY: str
CDN: str
GOOGLE_OAUTH_CLIENT_ID: str
GOOGLE_OAUTH_SECRET: str
PRODUCTION: bool
SESSION_SECRET: str
SRC_BACK: str


def from_cdn(location: str) -> str:
    return CDN + location


def get_globals(request: Request) -> Dict[str, str]:
    return json.dumps({
        'session': request.session,
    })


# Templating engine
TPL: Jinja2Templates
