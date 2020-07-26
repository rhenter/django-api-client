`Para visualizar o README em português <https://github.com/rhenter/django-api-client/blob/master/README.pt.rst>`_.


=================
Django API Client
=================

|PyPI latest| |PyPI Version| |PyPI License|  |CicleCI Status| |Coverage| |Docs|

Django API Client is a client for APIs in general, which allows iterating with the API as if they were using a Local model in their project, through a client and Custom CBV (Class based Views)


Some reasons to use the **Django API Client**

* If you work with microservices with APIs in multiple locations and want to continue using Django as a WebApp with the same capabilities to render data as if you were using native models

* You want to separate your Django project to let one of them only with the API with DRF and the other as a WebApp with Templates (HTML), CSS, JS instead of using some JS frontend (ReactJS, AngularJS, etc.)

* You want to use a third party API to list, create and change using the django template system

For more information, see our documentation at `Github Pages <https://rhenter.github.io/django-api-client/>`_

Requirements
============

- Python 3.x
- Django 2.0 or later


How to install
==============

You can get Django API Client by using pip:

.. code:: shell

    $ pip install django-api-client


If you want to install it from source, grab the git repository from Gitlab and run setup.py:

.. code:: shell

    $ git clone git@github.com:rhenter/django_api_client.git
    $ cd django_api_client
    $ python setup.py install


Config
======

To enable `django_api_client` in your project you need to add it to `INSTALLED_APPS` in your projects
`settings.py` file:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_api_client',
        ...
    )


Example
=======

- Also add the settings to access your API to settings.py:

.. code-block:: python

    DJANGO_API_CLIENT = {
      'API': [
        {
            'NAME': 'production',
            'URL_BASE': 'https://example.com/v1',
            'ENDPOINTS': [
                '/order/orders',
                '/user/users',
                ...
            ],
            'AUTHENTICATION_ACCESS_TOKEN': 'TOKEN'
        },
        {
            'NAME': 'localhost',
            'URL_BASE': 'http://localhost:8001/v1',
            'ENDPOINTS': [
                '/order/orders',
                '/user/users',
                ...
            ],
            'AUTHENTICATION_ACCESS_TOKEN': 'TOKEN'
        }
      ]
    }


*Note: The details of the configuration will be better explained in the documentation*

* Create a clients.py file in the core folder of your project, if you haven't, created it within your project folder to be simple to be imported from anywhere in the project with the following content:

.. code-block:: python

  from django_api_client.client import api_client_factory

  api_client = api_client_factory('production')


Note:
   - The name of this variable will be the name of the client that you can use throughout your project
   - It is recommended that the production use a set of configurations without configurations.py to change the simple way or the name of the API without the need to create several.
   - In our case, we have the option of "production" and "localhost", the factory generates the customer according to the name used and the parameters identified in it


* Now we are going to list the data using the normal Django template system

Let's imagine which client has a project folder (folder containing the settings.py file)

.. code-block:: python

  from django_api_client.mixins import ClientAPIListMixin

  from pasta_do_projeto.clients import api_client


  class OrderListView(ClientAPIListMixin):
      template_name = "template_name.html"        # Path where is your template
      page_title = 'Orders'                       # Generates a context variable to use in your template
      page_base_url = reverse_lazy('order:list')  # Information used in pagination, and the search
      paginate_by = 50                            # Number of items to generate the pagination
      client_method = api_client.order.get_orders


Note:
   The client will generate a user-friendly structure for each endpoint. Example with the endpoint */order/orders/*:

.. code-block:: text

    endpoint name: order
    methods:
         get_orders # GET: List
         get_order # GET: Detail of a resource using an identifier
         create_order # POST: Create a resource record
         update_order # PUT / PATCH: Fully or partially updates a resource using an identifier
    What does that mean?
      That the customer will always generate the structure according to the names of their endpoints

Documentation
=============

Check out the latest ``django-api-client`` documentation at `Github Pages <https://rhenter.github.io/django-api-client/>`_


Contributing
============

Please send pull requests, very much appreciated.


1. Fork the `repository <https://github.com/rhenter/django_api_client>`_ on GitHub.
2. Make a branch off of master and commit your changes to it.
3. Install requirements. ``pip install -r requirements-dev.txt``
4. Install pre-commit. ``pre-commit install``
5. Run the tests with ``cd test-django-project; py.test -vv -s``
6. Create a Pull Request with your contribution


.. |Docs| image:: https://img.shields.io/badge/Made%20with-Sphinx-1f425f.svg
   :target: https://rhenter.github.io/django-api-client/
.. |PyPI Version| image:: https://img.shields.io/pypi/pyversions/django-api-client.svg?maxAge=60
   :target: https://pypi.python.org/pypi/django-api-client
.. |PyPI License| image:: https://img.shields.io/pypi/l/django-api-client.svg?maxAge=120
   :target: https://github.com/rhenter/django-api-client/blob/master/LICENSE
.. |PyPI latest| image:: https://img.shields.io/pypi/v/django-api-client.svg?maxAge=120
   :target: https://pypi.python.org/pypi/django-api-client
.. |CicleCI Status| image:: https://circleci.com/gh/rhenter/django-api-client.svg?style=svg
   :target: https://circleci.com/gh/rhenter/django-api-client
.. |Coverage| image:: https://codecov.io/gh/rhenter/django-api-client/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/rhenter/django-api-client
