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
from starlette.responses import (
    JSONResponse,
)

# Constants
TFun = TypeVar('TFun', bound=Callable[..., Any])


def api_error_boundary(function: TFun) -> TFun:

    @wraps(function)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return await function(*args, **kwargs)
        except Exception as exc:
            return JSONResponse(
                content={
                    'error': f'{type(exc).__module__}.{type(exc).__name__}: {exc}',
                },
                status_code=400,
            )

    return wrapper
