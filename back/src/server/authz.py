# Standard library
from functools import (
    wraps,
)
from typing import (
    Any,
    Callable,
    NamedTuple,
    TypeVar,
)
from boto3.dynamodb.conditions import (
    Key,
)

# Third party libraries
from server import (
    persistence,
)
from starlette.requests import (
    Request,
)

# Constants
TFun = TypeVar('TFun', bound=Callable[..., Any])


def _does_user_have_a_session(request: Request) -> bool:
    return 'email' in request.session


def requires_session(function: TFun) -> TFun:

    @wraps(function)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        request: Request = args[0]

        if _does_user_have_a_session(request):
            return await function(*args, **kwargs)

        raise PermissionError('Session required, please authenticate first')

    return wrapper


def requires_session_sync(function: TFun) -> TFun:

    @wraps(function)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        request: Request = args[0]

        if _does_user_have_a_session(request):
            return function(*args, **kwargs)

        raise PermissionError('Session required, please authenticate first')

    return wrapper


class CachipfsAPIToken(NamedTuple):
    cachipfs_api_token: str
    cachipfs_encryption_key: str
    email: str


async def validate_cachipfs_api_token(request: Request) -> CachipfsAPIToken:
    cachipfs_api_token: str = request.headers.get('authorization')

    if not cachipfs_api_token:
        raise PermissionError('Missing Authorization header')

    data = await persistence.query(
        IndexName='cachipfs_api_token',
        KeyConditionExpression=(
            Key('cachipfs_api_token').eq(cachipfs_api_token)
        ),
        table=persistence.TableEnum.accounts,
    )

    if not data:
        raise PermissionError('Invalid API token')

    data = data[0]

    return CachipfsAPIToken(
        cachipfs_api_token=data['cachipfs_api_token'],
        cachipfs_encryption_key=data['cachipfs_encryption_key'],
        email=data['email'],
    )
