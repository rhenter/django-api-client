from .exceptions import AuthError, NotFound, ServerError, APIError
from .. import status


def validate_status_code(status_code):
    exception_class = None
    if status_code in (
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN):
        exception_class = AuthError(status_code,
                                    {'errorMessage': 'Authentication Error'})
    elif status_code == status.HTTP_404_NOT_FOUND:
        exception_class = NotFound(status_code,
                                   {'errorMessage': 'Endpoint Not Found'})
    elif status_code in range(status.HTTP_405_METHOD_NOT_ALLOWED, status.HTTP_417_EXPECTATION_FAILED + 1):
        exception_class = APIError(status_code)
    elif status.is_server_error(status_code):
        exception_class = ServerError(status_code)

    if exception_class:
        return False, exception_class
    return True, exception_class
