Using Class Based Views (CBV)
-----------------------------

ClientAPIListView
~~~~~~~~~~~~~~~~~

Following the same example as Model ListView, the results returned from the model will go to the context variable `` object_list``, unless you want to customize it. Using ClientAPIListView we will use the attribute `` client_method`` instead of `` model`` to get our results


.. code-block:: python

  from django_api_client.views import ClientAPIListView

  from folder_project.clients import api_client

  ...

  class TestListView(ClientAPIListView):
      template_name = "template_name.html"
      page_title = 'Tests'
      page_base_url = reverse_lazy('order:list')
      paginate_by = 50
      client_method = api_client.order.get_orders



.. hint::
  - template_name: path with name of you template
  - client_method: method of the client that to get the the resource list
  - page_title: Generates a context variable to use in your template
  - page_base_url: Information used in pagination, and the search
  - paginate_by: Number of items to generate the pagination

.. note::
  The usage example assumes that the endpoint ``/order/orders/``

ClientAPIDetailView
~~~~~~~~~~~~~~~~~~~

Following the same example as Model DetailView, the results returned from the model will go to the context variable ``object``, unless you want to customize it. Using ClientAPIDetailView we will use the attribute ``client_method`` instead of ``model`` to get our result

.. code-block:: python

  from django_api_client.views import ClientAPIDetailView

  from folder_project.clients import api_client

  ...

  class TestDetailView(ClientAPIDetailView):
      template_name = "template_name.html"
      page_title = _('View Test')
      client_method = api_client.order.get_order

.. hint::
  - template_name: path with name of you template
  - client_method: method of the client that to get the resource information
  - page_title: Generates a context variable to use in your template

.. note::
  The usage example assumes that the endpoint ``/order/orders/``

ClientAPICreateView
~~~~~~~~~~~~~~~~~~~

Following the same example as Model CreateView, on submit will validate and save, using ClientAPIListView we will use the attribute `` client_method`` instead of ``model`` to get our result

.. code-block:: python

  from django_api_client.views import ClientAPICreateView

  from folder_project.clients import api_client

  ...

  class TestCreateView(ClientAPICreateView):
      form_class = TestForm
      template_name = "template_name.html"
      page_title = _('View Test')
      success_url = reverse_lazy('test:list')
      client_method = api_client.order.create_order

.. hint::
  - template_name: path with name of you template
  - client_method: method of the client that to create
  - page_title: Generates a context variable to use in your template

.. note::
  The usage example assumes that the endpoint ``/order/orders/``

ClientAPIUpdateView
~~~~~~~~~~~~~~~~~~~

- Simple

.. code-block:: python

  from django_api_client.views import ClientAPIUpdateView

  from folder_project.clients import api_client

  ...

  class TestUpdateView(ClientAPIUpdateView):
      form_class = TestForm
      template_name = "template_name.html"
      success_url = reverse_lazy('test:list')
      page_title = _('Edit Test')
      client_method = api_client.order.update_order
      client_initial_method = api_client.order.update_order
      partial = False


- Advanced with a custom initial

.. code-block:: python

  from django_api_client.views import ClientAPIUpdateView

  from folder_project.clients import api_client

  ...

  class TestUpdateView(ClientAPIUpdateView):
      form_class = TestForm
      template_name = "template_name.html"
      success_url = reverse_lazy('test:list')
      page_title = _('Edit Test')
      client_method = api_client.order.update_order
      client_initial_method = api_client.order.update_order
      partial = False

      def get_initial(self):
          response = self.client_initial_method(**self.kwargs)
          data = response.as_dict()
          instance = response.as_obj()
          data['start_date'] = datetime.fromisoformat(instance.start_date).strftime('%d/%m/%Y %H:%M')
          data['end_date'] = datetime.fromisoformat(instance.end_date).strftime('%d/%m/%Y %H:%M')
          return data


.. hint::
    - template_name: path with name of you template
    - client_method: method of the client that to update
    - client_initial_method: method of the client that brings the result
    - page_title: Generates a context variable to use in your template
    - partial: means if you are going to update only part of your asset or you are going to update everything

.. note::
  The usage example assumes that the endpoint ``/order/orders/``


ClientAPIDeleteView
~~~~~~~~~~~~~~~~~~~

Following the same example as Model DetailView, the results returned from the model will go to the context variable ``object``, unless you want to customize it. Using ClientAPIDetailView we will use the attribute ``client_method`` instead of ``model`` to get our result

.. code-block:: python

  from django_api_client.views import ClientAPIDeleteView

  from folder_project.clients import api_client

  ...

  class TestDetailView(ClientAPIDeleteView):
      client_method = api_client.order.delete_order
      success_url = reverse_lazy('test:list')


.. hint::
  - client_method: method of the client that to remove the resource


.. note::
  The usage example assumes that the endpoint ``/order/orders/``