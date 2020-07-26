Available Settings
==================

There are some settings that can be easily configured and added to the settings

API
---

API key could be a dict with a single API or a List with Many API settings


* AUTHENTICATION_ACCESS_TOKEN

.. code-block:: text

  Definition: Used to pass your API Access Token
  Default: None
  Required: True

* AUTHENTICATION_ACCESS_TOKEN_TYPE

.. code-block:: text

  Definition: Key used on the Header Authorization. Could be ``Bearer``, ``Token``, etc
  Default: 'Bearer'
  Required: False

* AUTHENTICATION_METHOD

.. code-block:: text

  Definition: Method used to authentication. Today only ``header`` and ``url`` using params is available
  Default: 'header'
  Required: False

* AUTHENTICATION_URL_EXTRA_PARAMS

.. code-block:: text

  Definition: Extra params used to authenticate by URL using GET method
  Default: []
  Required: False

* AUTHENTICATION_URL_KEY

.. code-block:: text

  Definition: Key used to authenticate by URL using GET method
  Default: 'token'
  Required: False

* BASE_URL

.. code-block:: text

  Definition: API URL with the protocol. E.g: https://example.com/v1
  Default: None
  Required: True

* ENDPOINTS

.. code-block:: text

  Definition: Used to map all endpoint you want to access
  Default: []
  Required: False

* LOCALE

.. code-block:: text

  Definition: Only available in the Header authentication method, is the used to pass the ``Accept-Language`` in the request
  Default: Project Language Code
  Required: False

n')
* NAME

.. code-block:: text

  Definition: Used to pass your API Access Token
  Default: None
  Required: False

* URL_APPEND_SLASH

.. code-block:: text

  Definition: Used to pass your API Access Token
  Default: True
  Required: False

* TIMEOUT

.. code-block:: text

  Definition: Used to pass your API Access Token
  Default: 3
  Required: False


General defaults
----------------

* PAGE_SIZE

.. code-block:: text

  Definition: Used to pass your API Access Token
  Default: 100
  Required: False

* SLUG_FIELD

.. code-block:: text

  Definition: Key used to get a endpoint resource. Use the same identifier you receive in payload.
  Default: 'id'
  Required: False