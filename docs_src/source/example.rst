Example
=======

- Add this settings in your project ``settings.py`` file to access your API

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


.. note::
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

