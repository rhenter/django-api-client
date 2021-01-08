from django.http import Http404, HttpResponseForbidden, HttpResponseServerError


class APIError(Exception):
    """API Error Exception Class"""

    def __init__(
            self,
            status_code: str = '',
            resp_content: dict = None
    ) -> None:
        """APIError Exception raised when server returns error.
        Args:
            status_code (str): Status code retrieved from the server.
            resp_content (dict): Response's body with more detailed info about
                                 the problem that has occurred.

        """
        if resp_content:
            message = "API server returned [{}] status code".format(
                status_code)

            if "errorCode" in resp_content:
                message += ", and API returned [{}] error code".format(
                    resp_content["errorCode"])

            if "errorMessage" in resp_content:
                message += ", with message: ({})".format(
                    resp_content["errorMessage"])

        else:
            message = "API server returned a internal server error"

        super().__init__(message)


class APINotFound(Exception):
    pass


class APIUnreachableOrOffline(Exception):
    def __init__(self, exception_desc):
        self.exception_desc = exception_desc

        message = f"API server is offline or unreachable."
        if self.exception_desc:
            message = f"{message} Error {self.exception_desc}"
        super().__init__(message)


class AuthError(APIError, HttpResponseForbidden):
    pass


class NotFound(APIError, Http404):
    pass


class ServerError(APIError, HttpResponseServerError):
    """ServerError"""
    pass


class APIEndpointMissingArgument(Exception):
    pass
