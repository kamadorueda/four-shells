# Standard library
from functools import (
    wraps,
)
from typing import (
    Any,
    Callable,
    TypeVar,
)

# Third party libraries
from starlette.requests import (
    Request,
)

# Constants
TFun = TypeVar('TFun', bound=Callable[..., Any])


def requires_read_access_token(function: TFun) -> TFun:

    @wraps(function)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        request: Request = args[0]

        ns_id: str = request.path_params['id']
        token: str  =
        if _does_user_have_a_session(request):
            return await function(*args, **kwargs)

        raise PermissionError('Session required, please authenticate first')

    return wrapper
