Available Settings
==================

There are some settings that can be easily customized and added to the settings

API
---

``API`` key can be a dictionary in case it is just a single API or a list of dictionaries in case it is multiple APIs "


* AUTHENTICATION_ACCESS_TOKEN

.. note::
  - Definition: Used to pass your API Access Token
  - Default: None
  - Required: True

* AUTHENTICATION_ACCESS_TOKEN_TYPE

.. note::
  - Definition: Key used on the Header Authorization. Could be ``Bearer``, ``Token``, etc
  - Default: 'Bearer'
  - Required: False

* AUTHENTICATION_METHOD

.. note::
  - Definition: Method used to authentication. Today only ``header`` and ``url`` using params is available
  - Default: 'header'
  - Required: False

* AUTHENTICATION_URL_EXTRA_PARAMS

.. note::
  - Definition: Extra params used to authenticate by URL using GET method
  - Default: []
  - Required: False

* AUTHENTICATION_URL_KEY

.. note::
  - Definition: Key used to authenticate by URL using GET method
  - Default: 'token'
  - Required: False

* BASE_URL

.. note::
  - Definition: API URL with the protocol. E.g: https://example.com/v1
  - Default: None
  - Required: True

* ENDPOINTS

.. note::
  - Definition: Used to map all endpoint you want to access
  - Default: []
  - Required: False

* LOCALE

.. note::
  - Definition: Only available in the Header authentication method, is the used to pass the ``Accept-Language`` in the request
  - Default: Project Language Code set on settings.py
  - Required: False

* NAME

.. note::
  - Definition: Slug Name used to instantiate the client api factory
  - Default: None
  - Required: False

* URL_APPEND_SLASH

.. note::
  - Definition: Add a slash in end of the endpoint URL
  - Default: True
  - Required: False

* TIMEOUT

.. note::
  - Definition: Period to wait for the request response
  - Default: 3
  - Required: False


General defaults
----------------

* PAGE_SIZE

.. note::
  - Definition: Used to define the size of the Pagination
  - Default: 100
  - Required: False

* SLUG_FIELD

.. note::
  - Definition: Key used to get a endpoint record. Use the same identifier you receive in payload.
  - Default: 'id'
  - Required: False