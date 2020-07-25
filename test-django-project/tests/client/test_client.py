import pytest

from django_api_client.client import api_client_factory
from django_api_client.client.exceptions import APINotFound


def test_get_api_name_error():
    with pytest.raises(APINotFound) as error:
        api_client_factory('CRAZY NAME')

    assert str(error.value) == "API name Not Found."
