from typing import Tuple, Union

from .exceptions import APIError, AuthError, NotFound, ServerError
from .. import status


def validate_status_code(status_code: int) -> Union[
    Tuple[
        bool, Union[ServerError, APIError, NotFound, AuthError]],
    Tuple[
        bool, Union[ServerError, APIError, NotFound, AuthError, None]]
]:
    exception_class = None
    if status_code in (
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN):
        exception_class = AuthError(str(status_code), {'errorMessage': 'Authentication Error'})
    elif status_code == status.HTTP_404_NOT_FOUND:
        exception_class = NotFound(str(status_code), {'errorMessage': 'Endpoint Not Found'})
    elif status_code in range(status.HTTP_405_METHOD_NOT_ALLOWED, status.HTTP_417_EXPECTATION_FAILED + 1):
        exception_class = APIError(str(status_code))
    elif status.is_server_error(status_code):
        exception_class = ServerError(str(status_code), {'errorMessage': 'API experiencing difficulties. Try later.'})

    if exception_class:
        return False, exception_class
    return True, exception_class
