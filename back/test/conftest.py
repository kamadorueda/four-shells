# Standard library
# Third party libraries
from aioextensions import (
    run_decorator,
)
from base64 import (
    b64encode,
)
# Local libraries
import cli
from itsdangerous import (
    TimestampSigner,
)
import json
import os
import pytest
from starlette.testclient import (
    TestClient,
)

# Side effects
cli.main_config(
    data="~/.four-shells",
    debug=True,
)
cli.main_server_config(
    aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID_SERVER"],
    aws_cloudfront_domain=os.environ["AWS_CLOUDFRONT_DOMAIN"],
    aws_region=os.environ["AWS_REGION"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY_SERVER"],
    production=True,
    session_secret=os.environ["SERVER_SESSION_SECRET"],
)

# Local libraries
import config.server
from server import (
    asgi,
)


@pytest.fixture(scope="function")
def test_client() -> TestClient:
    client = TestClient(asgi.APP, raise_server_exceptions=False)

    return client
