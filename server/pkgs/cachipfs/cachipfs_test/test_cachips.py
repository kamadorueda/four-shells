# Third party libraries
from aioextensions import (
    run_decorator,
)

# Local libraries
from cachipfs import (
    accounts,
)


@run_decorator
async def test_functional(
    test_account_email,
) -> None:
    assert await accounts.ensure_account_exists(email=test_account_email)
