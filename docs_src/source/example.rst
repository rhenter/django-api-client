Example
=======

- Add this settings in your project ``settings.py`` file to access your API

.. code-block:: python


    DJANGO_API_CLIENT = {
        'API': [
          {
              'NAME': 'production',
              'BASE_URL': 'https://example.com/v1',
              'ENDPOINTS': [
                  '/order/orders',
                  '/user/users',
                  ...
              ],
              'AUTHENTICATION_ACCESS_TOKEN': 'TOKEN'
          },
          {
              'NAME': 'localhost',
              'BASE_URL': 'http://localhost:8001/v1',
              'ENDPOINTS': [
                  '/order/orders',
                  '/user/users',
                  ...
              ],
              'AUTHENTICATION_ACCESS_TOKEN': 'TOKEN'
          }
        ]
    }


.. hint::
  The details of the configuration will be better explained in the documentation

* Create a clients.py file in the core folder of your project, if you haven't, created it within your project folder to be simple to be imported from anywhere in the project with the following content:

.. code-block:: python

  from django_api_client.client import api_client_factory

  api_client = api_client_factory('production')


.. hint::
   - The name of this variable will be the name of the customer that you will import into every project
   - It is recommended that the name comes from a constant in the settings.py file, and if possible it can even be an environment variable.
   - In our case, we have 2 options,"production" and "localhost", the factory generates a `api client` according to the name used and the parameters identified in it


* Now we are going to list the data using the Django template system default

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
