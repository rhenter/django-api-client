import json
from urllib.parse import urljoin

import requests
from requests.exceptions import ConnectionError as RequestsConnectionError, ReadTimeout, Timeout

from django_api_client.utils import json_converter
from .exceptions import ServerError
from .factories import ResponseFactory
from .validators import validate_status_code


class RequestsTransport:
    def __init__(self, headers):
        self.session = requests.Session()
        self.session.headers.update(headers)

    def make_request(self, method_name, endpoint, **kwargs):
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
            api_name,
            base_url,
            access_token,
            access_token_type='Bearer',
            authentication_method='header',
            authentication_url_extra_params=None,
            authentication_url_key=None,
            locale='',
            timeout=3,
            transport_class=None,
            **kwargs):
        """
        Args:
            api_name (str): API name
            base_url (str): Provides the environment for  API.
            access_token (str): Specifies the access token.
            access_token_type (str): Type of the token, could be Bearer, Token, etc. Default is Bearer
            authentication_method (str): Method used to authenticate. Default is 'header'
            authentication_url_extra_params (dict): Extra params to authenticate by GET
            authentication_url_key (str): key to authenticate by URL. Default is token
            locale (str): Set the locale language. Default is pt-br
            timeout (int): Set the request timeout. Default is 3
            transport_class (obj): Class Request Sync or using AsyncIO
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

    def _set_transport_class(self, transport_class):
        headers = self.get_default_headers()
        self.transport = transport_class(headers=headers)

    def get_default_headers(self):
        """Get the required headers to access the API
        Optional:
            access_token_type (str): Specifies the access_token_type to be used on the request. E.g: Token or Bearer
            accept_language: Specifies the Accept-Language to be receive the response i18n.
        Returns:
             dict: Authorization and Content Type
        """
        return {
            'Authorization': f'{self.access_token_type} {self.access_token}',
            'Content-Type': 'application/json',
            "Accept-Language": self.accept_language
        }

    def make_request(self, method_name, endpoint, **kwargs):
        """Requests data from the API.
        Args:
            endpoint (str): URL for the API endpoint.
            method_name (str): Specifies the method to be used on the request.
        Optional:
            params (dict, optional): Specifies parameters to be sent with the
            request.

        Returns:
            response: Requests response object.
        """

        full_url = urljoin(self.base_url, endpoint)

        try:
            response = self.transport.make_request(
                method_name, full_url, timeout=self.timeout, **kwargs
            )
        except (Timeout, ReadTimeout, RequestsConnectionError) as exc:
            raise ServerError() from exc

        is_valid, exception_class = validate_status_code(response.status_code)
        if not is_valid:
            raise exception_class

        return response

    def create(self, endpoint, data):
        """Do a POST without need to pass all arguments to make a request
        Args:
            endpoint (str): URL for the API endpoint.
            data (dict, list of tuples): Data to send in the body of the request.

        Returns:
            dict: Data retrieved for specified endpoint.
        """
        response = self.make_request('POST', endpoint, data=json.dumps(data, default=json_converter))
        return ResponseFactory(response, endpoint)

    def update(self, endpoint, data, partial=False):
        """Do a update (PUT/PATCH) without need to pass all arguments to make a request
        Args:
            endpoint (str): URL for the API endpoint.
            data (dict, list of tuples): Data to send in the body of the request.
            partial (bool): To specify whether the update will change everything
                            or just a few attributes. Default is False

        Returns:
            dict: Data retrieved for specified endpoint.
        """
        method = 'PATCH' if partial else 'PUT'
        response = self.make_request(method, endpoint, data=json.dumps(data, default=json_converter))
        return ResponseFactory(response, endpoint)

    def search(self, endpoint, **kwargs):
        """Do a GET to make a search without need
           to pass all arguments to make a request.
        Args:
            endpoint (str): URL for the API endpoint.
        Kwargs(Optional):
            params (dict): Specifies parameters to be sent with the request.

        Returns:
            dict: Data retrieved for specified endpoint.
        """
        params = kwargs.pop('params', {})
        response = self.make_request('GET', endpoint, params=params)
        return ResponseFactory(response, endpoint)

    def delete(self, endpoint):
        """Do a DELETE request to remove a resource
        Args:
            endpoint (str): URL for the API endpoint with the ID of the resource.

        Returns:
            dict: Empty
        """
        response = self.make_request('DELETE', endpoint)
        return ResponseFactory(response, endpoint)


class BaseEndpoint:
    """Class holding endpoint functions.
    """

    def __init__(self, api, endpoint=''):
        self._api = api
        self.endpoint = endpoint
        self.endpoint_name = self._get_endpoint_name()

    def _get_endpoint_name(self):
        words = [key for key in self.endpoint.split('?')[0].split('/') if key]
        response_name = words[-1]
        if '-' in response_name:
            response_name = response_name.replace('-', '_')
        elif response_name.endswith('s'):
            response_name = response_name[:-1]
        return response_name

    def list(self, **kwargs):
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

        endpoint = f'{self.endpoint}'
        return self._api.search(endpoint, **kwargs)

    def get(self, object_id):
        """Get the full details for a single resource
        Args:
            object_id (str): Object ID.

        Returns:
            dict: Full resource details.

        Raises:
            RequestException: An error thrown by Requests library.
            ValueError: An error thrown by json parser, if JSON decoding fails.
            APIError: An error occurred while requesting the API.

        """
        path = f'{self.endpoint}/{object_id}/'
        if self.endpoint.endswith('/'):
            path = f'{self.endpoint}{object_id}/'
        return self._api.search(path)

    def create(self, data):
        """Update a single Object.

        Args:
            data (dict, list of tuples): Data to send in the body of the request.

        Returns:
            dict: Data retrieved for specified endpoint.

        Raises:
            RequestException: An error thrown by Requests library.
            ValueError: An error thrown by json parser, if JSON decoding fails.
            APIError: An error occurred while requesting the API.

        """
        endpoint = f'{self.endpoint}'
        return self._api.create(endpoint, data)

    def update(self, object_id, data, partial=False):
        """Update a single Object.

        Args:
            object_id (str): Object ID.
            data (dict, list of tuples): Data to send in the body of the request.
            partial (bool): To specify whether the update will change everything
                            or just a few attributes. Default is False

        Returns:
            dict: Data retrieved for specified endpoint.

        Raises:
            RequestException: An error thrown by Requests library.
            ValueError: An error thrown by json parser, if JSON decoding fails.
            APIError: An error occurred while requesting the API.

        """
        path = f'{self.endpoint}/{object_id}/'
        if self.endpoint.endswith('/'):
            path = f'{self.endpoint}{object_id}/'
        return self._api.update(path, data, partial)

    def delete(self, object_id):
        """Delete a single resource
        Args:
            object_id (str): Object ID.

        Returns:
            dict: Empty

        Raises:
            RequestException: An error thrown by Requests library.
            APIError: An error occurred while requesting the API.
        """
        path = f'{self.endpoint}/{object_id}/'
        if self.endpoint.endswith('/'):
            path = f'{self.endpoint}{object_id}/'
        return self._api.delete(path)
