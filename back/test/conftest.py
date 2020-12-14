# Standard library
from base64 import (
    b64encode,
)
import json
import os

# Third party libraries
import pytest
from itsdangerous import (
    TimestampSigner,
)
from starlette.testclient import (
    TestClient,
)

# Local libraries
import cli

# Side effects
cli.main_config(
    data='~/.four-shells',
    debug=True,
)
cli.main_server_config(
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID_SERVER'],
    aws_cloudfront_domain=os.environ['AWS_CLOUDFRONT_DOMAIN'],
    aws_region=os.environ['AWS_REGION'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY_SERVER'],
    production=True,
    google_oauth_client_id=os.environ['GOOGLE_OAUTH_CLIENT_ID_SERVER'],
    google_oauth_secret=os.environ['GOOGLE_OAUTH_SECRET_SERVER'],
    session_secret=os.environ['SERVER_SESSION_SECRET'],
)

# Local libraries
import config.server
from server import (
    asgi,
)

def _login(client: TestClient, email: str) -> None:
    signer = TimestampSigner(config.server.SESSION_SECRET)

    session_cookie = signer.sign(b64encode(json.dumps({
        'email': email,
    }).encode())).decode()

    client.cookies[config.server.SESSION_COOKIE] = session_cookie


@pytest.fixture(scope='session')
def test_account_email() -> str:
    return 'test@4shells.com'


@pytest.fixture(scope='function')
def test_client() -> TestClient:
    client = TestClient(asgi.APP, raise_server_exceptions=False)

    return client


@pytest.fixture(scope='function')
def test_client_raiser() -> TestClient:
    client = TestClient(asgi.APP)

    return client


@pytest.fixture(scope='function')
def test_client_with_session(test_account_email: str) -> TestClient:
    client = TestClient(asgi.APP, raise_server_exceptions=False)
    _login(client, test_account_email)

    return client


@pytest.fixture(scope='function')
def test_client_session(test_account_email: str) -> TestClient:
    client = TestClient(asgi.APP)
    _login(client, test_account_email)

    return client
