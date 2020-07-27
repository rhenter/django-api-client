Using Function Based Views (FBV)
--------------------------------

Using function-based views, the way is somewhat manual but it is quite simple to use the results in the same way.

List
~~~~

.. code-block:: python


  from folder_project.clients import api_client

  ...

  def get_orders(request):
    response = api_client.order.orders.list()
    template = 'fbv/list.html'
    context = {"object_list": response.as_obj().results}
    return render(request, template, context)


.. note::
  The usage example assumes that the endpoint ``/order/orders/``
  Waiting the response {'count': , 'next': None, 'previous': None, 'results': []}

Detail
~~~~~~

.. code-block:: python


  from folder_project.clients import api_client

  ...

  def get_order(request, pk):
    response = api_client.order.orders.get(id=pk)
    template = 'fbv/detail.html'
    context = {"object": response.as_obj()}
    return render(request, template, context)


.. note::
  The usage example assumes that the endpoint ``/order/orders/``


Create
~~~~~~

.. code-block:: python


  from folder_project.clients import api_client

  ...

  def create_order(request, pk):
    template = 'fbv/form.html'

    form = TestForm(request.POST or None)
    if form.is_valid():
        response = api_client.order.orders.create(data=form.cleaned_data)
        return redirect('fbv:index')

    context = {"form": form}
    return render(request, template, context)


.. note::
  The usage example assumes that the endpoint ``/order/orders/``

Update
~~~~~~

.. code-block:: python


  from folder_project.clients import api_client

  ...

  def update_order(request, pk):
    template = 'fbv/form.html'
    response = api_client.order.get_order(id=pk)

    form = TestForm(request.POST or None, initial=response.as_dict())
    if form.is_valid():
        response = api_client.order.orders.update(id=pk, data=form.cleaned_data, partial=False)
        return redirect('fbv:index')

    context = {
      "object": response.as_obj(),
      "form": form
     }
    return render(request, template, context)


.. note::
  The usage example assumes that the endpoint ``/order/orders/``


Delete
~~~~~~

.. code-block:: python


  from folder_project.clients import api_client

  ...
  def delete_order(request, pk):
      template = 'fbv/delete.html'
      response = api_client.order.orders.get(id=pk)
      if request.method == 'POST':
          api_client.order.orders.delete(id=pk)
          return redirect('fbv:index')
      context = {"object": response.as_obj()}
      return render(request, template, context)

.. note::
  The usage example assumes that the endpoint ``/order/orders/``
