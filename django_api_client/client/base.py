import json
from typing import Any
from urllib.parse import urljoin

import requests
from django.utils.translation import gettext_lazy as _
from requests.exceptions import ConnectionError as RequestsConnectionError, ReadTimeout, Timeout

from django_api_client.utils import json_converter
from .exceptions import APIEndpointMissingArgument, APIUnreachableOrOffline
from .factories import ResponseFactory
from .validators import validate_status_code


class RequestsTransport:
    def __init__(self, headers: Any) -> None:
        self.session = requests.Session()
        self.session.headers.update(headers)

    def make_request(self, method_name: str, endpoint: str, **kwargs: Any) -> Any:
        method = getattr(self.session, method_name.lower())
        return method(endpoint, **kwargs)


class BaseAPI:
    """
    BaseAPI Abstract object.
    Attributes:
        base_url: URL from API
        timeout: Request timeout
        token:  API Access token
        transport: Transport class to able to use Requests
    """

    def __init__(
            self,
            api_name: str,
            base_url: str,
            access_token: str,
            access_token_type: str = 'Bearer',
            authentication_method: str = 'header',
            authentication_url_extra_params: dict = None,
            authentication_url_key: str = None,
            locale: str = '',
            timeout: int = 3,
            transport_class: Any = None,
            **kwargs: Any
    ) -> None:
        """
        Args:
            api_name: API name
            base_url: Provides the environment for  API.
            access_token: Specifies the access token.
            access_token_type: Type of the token, could be Bearer, Token, etc. Default is Bearer
            authentication_method: Method used to authenticate. Default is 'header'
            authentication_url_extra_params: Extra params to authenticate by GET
            authentication_url_key: key to authenticate by URL. Default is token
            locale: Set the locale language. Default is pt-br
            timeout: Set the request timeout. Default is 3
            transport_class: Class Request Sync or using AsyncIO
        """
        self.access_token = access_token
        self.accept_language = locale
        self.access_token_type = access_token_type
        self.api_name = api_name
        self.authentication_method = authentication_method
        self.authentication_url_extra_params = authentication_url_extra_params
        self.authentication_url_key = authentication_url_key
        self.base_url = base_url
        self.timeout = timeout
        self._set_transport_class(transport_class=transport_class or RequestsTransport)
        self.kwargs = kwargs

    def _render_response(self, response: Any, endpoint: Any) -> ResponseFactory:
        return ResponseFactory(response, endpoint)

    def _set_transport_class(self, transport_class: Any) -> None:
        headers = self.get_default_headers()
        self.transport = transport_class(headers=headers)

    def get_default_headers(self) -> dict:
        """Get the required headers to access the API
        Optional:
            access_token_type: Specifies the access_token_type to be used on the request. E.g: Token or Bearer
            accept_language: Specifies the Accept-Language to be receive the response i18n.
        Returns:
             dict: Authorization and Content Type
        """
        return {
            'Authorization': f'{self.access_token_type} {self.access_token}',
            "Accept-Language": self.accept_language
        }

    def make_request(self, method_name: str, endpoint: str, **kwargs: Any) -> Any:
        """Requests data from the API.
        Args:
            endpoint: URL for the API endpoint.
            method_name: Specifies the method to be used on the request.
        Optional:
            params (dict, optional): Specifies parameters to be sent with the
            request.

        Returns:
            response: Requests response object.
        """

        full_url = urljoin(self.base_url, endpoint)

        content_type = kwargs.pop('content_type', 'application/json')
        if content_type != 'form-data':
            self.transport.session.headers['Content-Type'] = content_type

        json = None
        if content_type == 'application/json':
            json = 'json'

        try:
            response = self.transport.make_request(
                method_name, full_url, timeout=self.timeout, json=json, **kwargs
            )
        except (Timeout, ReadTimeout, RequestsConnectionError) as exc:
            raise APIUnreachableOrOffline(exception_desc=str(exc)) from exc

        is_valid, exception_class = validate_status_code(response.status_code)
        if not is_valid:
            raise exception_class

        return response

    def create(
            self,
            endpoint: str,
            data: dict = None,
            files: dict = None,
            content_type: str = 'application/json'
    ) -> ResponseFactory:
        """Do a POST without need to pass all arguments to make a request
        Args:
            endpoint: URL for the API endpoint.
            data: Data to send in the body of the request.
            files: Files to send in the body of the request.
            content_type: Request Content Type. E.g: 'application/json', 'form-data'

        Returns:
            dict: Data retrieved for specified endpoint.
        """
        if content_type == 'application/json' or not files:
            data = json.dumps(data, default=json_converter)
        response = self.make_request('POST', endpoint, data=data, files=files, content_type=content_type)
        return self._render_response(response, endpoint)

    def update(
            self,
            endpoint: str,
            data: dict = None,
            files: dict = None,
            partial: bool = False,
            content_type: str = 'application/json'
    ) -> ResponseFactory:
        """Do a update (PUT/PATCH) without need to pass all arguments to make a request
        Args:
            endpoint: URL for the API endpoint.
            data: Data to send in the body of the request.
            files: Files to send in the body of the request.
            content_type: Request Content Type. E.g: 'application/json', 'form-data'
            partial: To specify whether the update will change everything
                     or just a few attributes. Default is False

        Returns:
            dict: Data retrieved for specified endpoint.
        """
        method = 'PATCH' if partial else 'PUT'
        if content_type == 'application/json':
            data = json.dumps(data, default=json_converter)

        if files:
            response = self.make_request(method, endpoint, data=data, files=files, content_type=content_type)
            return self._render_response(response, endpoint)

        response = self.make_request(method, endpoint, data=data, content_type=content_type)
        return self._render_response(response, endpoint)

    def search(self, endpoint: str, **kwargs: Any) -> ResponseFactory:
        """Do a GET to make a search without need
           to pass all arguments to make a request.
        Args:
            endpoint: URL for the API endpoint.
        Kwargs(Optional):
            params (dict): Specifies parameters to be sent with the request.

        Returns:
            dict: Data retrieved for specified endpoint.
        """
        params = kwargs.pop('params', {})
        response = self.make_request('GET', endpoint, params=params)
        return self._render_response(response, endpoint)

    def delete(self, endpoint: str) -> ResponseFactory:
        """Do a DELETE request to remove a resource
        Args:
            endpoint: URL for the API endpoint with the ID of the resource.

        Returns:
            dict: Empty
        """
        response = self.make_request('DELETE', endpoint)
        return self._render_response(response, endpoint)


class BaseEndpoint:
    """Class holding endpoint functions.
    """

    def __init__(self, api: Any, endpoint: str = '') -> None:
        self._api = api
        self.endpoint = endpoint
        self.endpoint_name = self._get_endpoint_name()

    def __repr__(self) -> str:
        return f'<BaseEndpoint {self.endpoint_name}: {self.endpoint}>'

    def __str__(self) -> str:
        return f'{self.endpoint_name} -> {self.endpoint}'

    def _get_endpoint_name(self) -> str:
        words = [key for key in self.endpoint.split('?')[0].split('/') if key]
        response_name = words[-1]
        if '-' in response_name:
            response_name = response_name.replace('-', '_')
        elif response_name.endswith('s'):
            response_name = response_name[:-1]
        return response_name

    def get_endpoint(self, object_id: Any = None, detail: bool = False, *args: Any, **kwargs: Any) -> str:
        if detail:
            if not object_id:
                raise APIEndpointMissingArgument(_('Identifier is required.'))
            path = f'{self.endpoint}/{object_id}/'
            if self.endpoint.endswith('/'):
                path = f'{self.endpoint}{object_id}/'
        else:
            path = self.endpoint

        if all([c in path for c in ['{', '}']]):
            try:
                path = path.format(**kwargs)
            except KeyError:
                raise APIEndpointMissingArgument(
                    _('This endpoint contains a Arg in the path and this Arg is required.'))
        return path

    def list(self, *args: Any, **kwargs: Any) -> ResponseFactory:
        """Get a list of all Objects of a Resource.

        Args:
            This function takes no arguments.

        Returns:
            dict: Objects of a Resource.

        Raises:
            RequestException: An error thrown by Requests library.
            ValueError: An error thrown by json parser, if JSON decoding fails.
            APIError: An error occurred while requesting the API endpoint.
        """

        endpoint = self.get_endpoint(*args, **kwargs)
        return self._api.search(endpoint, **kwargs)

    def get(self, object_id: str, *args: Any, **kwargs: Any) -> ResponseFactory:
        """Get the full details for a single resource
        Args:
            object_id: Object ID.

        Returns:
            dict: Full resource details.

        Raises:
            RequestException: An error thrown by Requests library.
            ValueError: An error thrown by json parser, if JSON decoding fails.
            APIError: An error occurred while requesting the API.

        """
        endpoint = self.get_endpoint(object_id, detail=True, *args, **kwargs)
        return self._api.search(endpoint)

    def create(
            self,
            data: dict = None,
            files: dict = None,
            content_type: str = 'application/json',
            *args: Any,
            **kwargs: Any
    ) -> ResponseFactory:

        """Update a single Object.

        Args:
            data: Data to send in the body of the request.
            files: Files to send in the body of the request.
            content_type: Request Content Type. E.g: 'application/json', 'form-data'

        Returns:
            dict: Data retrieved for specified endpoint.

        Raises:
            RequestException: An error thrown by Requests library.
            ValueError: An error thrown by json parser, if JSON decoding fails.
            APIError: An error occurred while requesting the API.

        """
        endpoint = self.get_endpoint(*args, **kwargs)
        return self._api.create(endpoint, data=data, files=files, content_type=content_type)

    def update(
            self,
            object_id: Any,
            data: dict = None,
            files: dict = None,
            partial: bool = False,
            content_type: str = 'application/json',
            *args: Any,
            **kwargs: Any
    ) -> ResponseFactory:
        """Update a single Object.

        Args:
            object_id: Object ID.
            data: Data to send in the body of the request.
            files: Files to send in the body of the request.
            content_type: Request Content Type. E.g: 'application/json', 'form-data'
            partial: To specify whether the update will change everything
                            or just a few attributes. Default is False

        Returns:
            dict: Data retrieved for specified endpoint.

        Raises:
            RequestException: An error thrown by Requests library.
            ValueError: An error thrown by json parser, if JSON decoding fails.
            APIError: An error occurred while requesting the API.

        """
        endpoint = self.get_endpoint(object_id, detail=True, *args, **kwargs)
        return self._api.update(endpoint, data=data, files=files, partial=partial, content_type=content_type)

    def delete(self, object_id: Any, *args: Any, **kwargs: Any) -> ResponseFactory:
        """Delete a single resource
        Args:
            object_id: Object ID.

        Returns:
            dict: Empty

        Raises:
            RequestException: An error thrown by Requests library.
            APIError: An error occurred while requesting the API.
        """
        endpoint = self.get_endpoint(object_id, detail=True, *args, **kwargs)
        return self._api.delete(endpoint)
