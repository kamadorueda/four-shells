# Standard library
from functools import (
    wraps,
)
# Third party libraries
from starlette.requests import (
    Request,
)
from typing import (
    Any,
    Callable,
    NamedTuple,
    TypeVar,
)

# Constants
TFun = TypeVar("TFun", bound=Callable[..., Any])


def _does_user_have_a_session(request: Request) -> bool:
    return "email" in request.session


def requires_session(function: TFun) -> TFun:
    @wraps(function)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        request: Request = args[0]

        if _does_user_have_a_session(request):
            return await function(*args, **kwargs)

        raise PermissionError("Session required, please authenticate first")

    return wrapper


def requires_session_sync(function: TFun) -> TFun:
    @wraps(function)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        request: Request = args[0]

        if _does_user_have_a_session(request):
            return function(*args, **kwargs)

        raise PermissionError("Session required, please authenticate first")

    return wrapper
