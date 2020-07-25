from unittest.mock import Mock

import pytest

from django_api_client import status
from django_api_client.client.exceptions import APIError, AuthError, NotFound, ServerError
from django_api_client.client.validators import validate_status_code


@pytest.mark.parametrize('expected,status_code,expected_exception', [
    (False, status.HTTP_401_UNAUTHORIZED, AuthError),
    (False, status.HTTP_417_EXPECTATION_FAILED, APIError),
    (False, status.HTTP_404_NOT_FOUND, NotFound),
    (False, status.HTTP_500_INTERNAL_SERVER_ERROR, ServerError),
])
def test_validate_status_invalid(expected, status_code, expected_exception):
    is_valid, exception_class = validate_status_code(status_code)
    assert is_valid == expected
    assert isinstance(exception_class, expected_exception)


def test_validate_status_valid():
    is_valid, exception_class = validate_status_code(status.HTTP_200_OK)
    assert is_valid
    assert not exception_class


def test_validate_status_with_api_code(api_client):
    api_client.api.transport.make_request = Mock(
        side_effect=APIError('401', {'errorCode': '999'})
    )
    with pytest.raises(APIError) as error:
        api_client.api.search('http://example.com/test')

    expected = 'API server returned [401] status code, and API returned [999] error code'
    assert str(error.value) == expected
