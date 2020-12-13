# Standard library
from base64 import (
    b64encode,
)
import json

# Third party libraries
import pytest
from itsdangerous import (
    TimestampSigner,
)
from starlette.testclient import (
    TestClient,
)

# Local libraries
from server import (
    asgi,
    config,
)

def _login(client: TestClient, email: str) -> None:
    signer = TimestampSigner(config.SESSION_SECRET)

    session_cookie = signer.sign(b64encode(json.dumps({
        'email': email,
    }).encode())).decode()

    client.cookies[config.SESSION_COOKIE] = session_cookie


@pytest.fixture(autouse=True, scope='session')
def test_account_email() -> str:
    return 'test@4shells.com'


@pytest.fixture(autouse=True, scope='function')
def test_client() -> TestClient:
    client = TestClient(asgi.APP, raise_server_exceptions=False)

    return client


@pytest.fixture(autouse=True, scope='function')
def test_client_raiser() -> TestClient:
    client = TestClient(asgi.APP)

    return client


@pytest.fixture(autouse=True, scope='function')
def test_client_with_session(test_account_email: str) -> TestClient:
    client = TestClient(asgi.APP, raise_server_exceptions=False)
    _login(client, test_account_email)

    return client


@pytest.fixture(autouse=True, scope='function')
def test_client_session(test_account_email: str) -> TestClient:
    client = TestClient(asgi.APP)
    _login(client, test_account_email)

    return client
