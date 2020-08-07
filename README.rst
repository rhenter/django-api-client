`Para visualizar o README em português <https://github.com/rhenter/django-api-client/blob/master/README.pt.rst>`_.


=================
Django API Client
=================

|PyPI latest| |PyPI Version| |PyPI License|  |CicleCI Status| |Coverage| |Docs| |Open Source? Yes!|

The Django API Client is an API response wrapper, which translates Django's native calls when using a view to a particular REST API. Whether using the API client directly in a FBV (Function-based View) or using CBV (Class-based View), this library makes this communication as transparent and easy as possible

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


If you want to install it from source, grab the git repository from GitHub and run setup.py:

.. code:: shell

    $ git clone git@github.com:rhenter/django_api_client.git
    $ cd django_api_client
    $ python setup.py install


Settings
========

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
            'BASE_URL': 'https://example.com',
            'ENDPOINTS': [
                '/v1/order/orders',
                '/v1/user/users',
                ...
            ],
            'AUTHENTICATION_ACCESS_TOKEN': 'TOKEN'
        },
        {
            'NAME': 'localhost',
            'BASE_URL': 'http://localhost:8001',
            'ENDPOINTS': [
                '/v1/order/orders',
                '/v1/user/users',
                ...
            ],
            'AUTHENTICATION_ACCESS_TOKEN': 'TOKEN'
        }
      ]
    }


.. note::
  The details of the configuration will be better explained in the documentation

* Create a clients.py file in the core folder of your project, if you haven't, created it within your project folder to be simple to be imported from anywhere in the project with the following content:

.. code-block:: python

  from django_api_client.client import api_client_factory

  api_client = api_client_factory('production')


.. note::
   - The name of this variable will be the name of the client that you can use throughout your project
   - It is recommended that the production use a set of configurations without configurations.py to change the simple way or the name of the API without the need to create several.
   - In our case, we have the option of "production" and "localhost", the factory generates the customer according to the name used and the parameters identified in it


* Now we are going to list the data using the normal Django template system

Let's imagine which client is located in a folder called clients on project folder (folder containing the settings.py file)

.. code-block:: python

  from django_api_client.mixins import ClientAPIListMixin

  from pasta_do_projeto.clients import api_client


  class OrderListView(ClientAPIListMixin):
      template_name = "template_name.html"        # Path where is your template
      page_title = 'Orders'                       # Generates a context variable to use in your template
      page_base_url = reverse_lazy('order:list')  # Information used in pagination, and the search
      paginate_by = 50                            # Number of items to generate the pagination
      client_method = api_client.order.orders.list


.. note::
   The client will generate a user-friendly structure for each endpoint. Example with the endpoint */order/orders/*:


In your template you can use the forms and pagination snippets. E.g:


.. code-block:: jinja

    {% content %}

    ...
    <div class="card card-navy card-outline">
      <div class="card-header">
        <h3 class="card-title">
          {% trans "Order List" %} : <small class="text-muted">{{ paginator.count }}</small>
        </h3>
        {% include "includes/form_paginate_by.html" with paginate_by=paginate_by range_pagination=range_pagination %}
        {% include "includes/form_search.html" with search=search %}
      </div>
      <div class="card-body table-responsive p-0">
        <table class="table table-bordered table-hover table-striped" id="list-content">
          <thead>
          <tr>
            <th>{% trans 'Code' %}</th>
            <th>{% trans 'Customer' %}</th>
            <th>{% trans 'Product' %}</th>
          </tr>
          </thead>
          <tbody class="text-gray">
          {% for order in object_list %}
            <tr>
              <td><a href="{% url 'order:detail' pk=order.id %}" </a>
              </td>
              <td>{{ order.id }}</td>
              <td>{{ order.customer.name|title }}</td>
              <td>{{ order.product.name|title }}</td>
            </tr>
            {% endfor %}
          {% endif %}
          </tbody>
        </table>
      </div>
      <div class="card-footer">
        {% if object_list|length != 0 or not object_list %}
          {% include "includes/list_paginator.html" with page_obj=page_obj paginator=paginator %}
        {% endif %}
      </div>
    </div>


.. note::
  - Example using Bootstrap Styles(CSS)
  - includes/form_search.html: Form with search input. This ``include`` support placeholder too.
  - includes/form_paginate_by.html: Select form to choose how many elements the page will be paginate. Ex: by (20, 40, 60, etc ...)
  - includes/list_paginator.html: Block with pagination elements with the number of pages buttons, previous and next


.. code-block:: text

    endpoint name: order
    methods:
         - list   # GET: List
         - get    # GET: Detail of a resource using an identifier
         - create # POST: Create a resource record
         - update # PUT / PATCH: Fully or partially updates a resource using an identifier
         - delete # DELETE: delete a record in a resource using an identifier

.. hint::

    What does that mean?
      That the API Client will always generate the structure according to the names of their endpoints

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


.. |Docs| image:: https://img.shields.io/static/v1?label=DOC&message=GitHub%20Pages&color=%3CCOLOR%3E
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
.. |Open Source? Yes!| image:: https://badgen.net/badge/Open%20Source%20%3F/Yes%21/blue?icon=github
   :target: https://github.com/rhenter/django-api-client
