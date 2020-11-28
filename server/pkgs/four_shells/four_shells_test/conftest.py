# Third party libraries
import pytest


@pytest.fixture(autouse=True, scope='session')
def test_account_email() -> str:
    return 'test@4shells.com'
