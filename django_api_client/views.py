import json

from django.core.paginator import InvalidPage
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, ListView
from django.views.generic.edit import DeleteView, FormView

from . import status
from .mixins import BaseViewMixin
from .paginators import ClientAPIPagination
from .settings import api_client_settings
from .utils import clean_url


class ClientAPIFormView(FormView):
    slug_field = api_client_settings.configs['SLUG_FIELD']
    slug_url_kwarg = api_client_settings.configs['SLUG_FIELD']
    client_method = None

    def send_cleaned_data(self, response, form, update=False):
        response_status = status.HTTP_201_CREATED
        if update:
            response_status = status.HTTP_200_OK
        if response.raw.status_code != response_status:
            errors = response.raw.json()
            for error_key in errors:
                if error_key == 'non_field_errors':
                    form.add_error(None, errors[error_key])
                    continue
                form.add_error(error_key, errors[error_key])

            if self.request.is_ajax():
                return JsonResponse({'errors': form.errors})
            return self.form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse({'status': True})
        return super().form_valid(form)


class ClientAPIAuthenticatedCreateView(ClientAPIFormView):

    def form_valid(self, form):
        response = self.client_method(data=form.cleaned_data)
        return self.send_cleaned_data(response, form)


class ClientAPIAuthenticatedUpdateView(ClientAPIFormView):
    client_initial_method = None
    partial = False

    def get_initial(self):
        if not self.client_initial_method:
            return None
        response = self.client_initial_method(self.kwargs.get(self.slug_field))
        return response.as_dict()

    def form_valid(self, form):
        params = {
            'data': form.cleaned_data,
            'partial': self.partial
        }
        response = self.client_method(self.kwargs.get(self.slug_field), **params)
        return self.send_cleaned_data(response, form, update=True)


class ClientAPIAuthenticatedListView(ListView):
    http_method_names = ['get']
    paginate_by = api_client_settings.configs['PAGE_SIZE']
    paginator_class = ClientAPIPagination
    client_method = None
    client_method_result_key = 'results'
    extra_kwargs = []
    page_base_url = ''
    page_title = ''

    def get_paginate_by(self):
        """
        Get the number of items to paginate by, or ``None`` for no pagination.
        """
        return int(self.request.GET.get('paginate_by', self.paginate_by))

    def get_page_base_url(self):
        return self.page_base_url or self.request.path

    def _paginate_queryset(self, client_method, page_size, **kwargs):
        """Paginate the queryset, if needed."""
        extra_params = kwargs.get('extra_params', {})
        paginator = self.paginator_class(client_method, page_size, extra_params=extra_params)
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1
        try:
            page_number = int(page)
        except ValueError:
            if page == 'last':
                page_number = paginator.num_pages
            else:
                raise Http404(_('Page is not “last”, nor can it be converted to an int.'))
        try:
            page = paginator.page(page_number)
            return paginator, page, page.object_list, page.has_other_pages()
        except InvalidPage as e:
            raise Http404(_('Invalid page (%(page_number)s): %(message)s') % {
                'page_number': page_number,
                'message': str(e)
            })

    def get_extra_params(self, request):
        default_kwargs_list = ['search']
        default_kwargs_list.extend(self.extra_kwargs)
        extra_params = {}
        for param in default_kwargs_list:
            param_value = request.GET.get(param, '')
            if param_value:
                extra_params[param] = param_value
        return extra_params

    def get_context_data(self, **kwargs):
        filter_params = kwargs.pop('filter_params', False)
        paginate_by = self.get_paginate_by()
        if paginate_by:
            paginator, page, queryset, is_paginated = self._paginate_queryset(self.client_method,
                                                                              paginate_by,
                                                                              extra_params=kwargs)
            context = {
                'paginator': paginator,
                'page_obj': page,
                'is_paginated': is_paginated,
                'object_list': queryset
            }
        else:
            context = {
                'paginator': None,
                'page_obj': None,
                'is_paginated': False,
                'object_list': self.object_list
            }

        search_url = clean_url(self.request.get_full_path())
        context.update({
            'search': self.request.GET.get('search', ''),
            'search_url': search_url,
            'filter_params': filter_params,
            'page_base_url': self.get_page_base_url(),
            'range_pagination': [x for x in range(20, 220, 20)],
            'paginate_by': paginate_by,
            'page_title': self.page_title
        })

        pagination_params = ['search', 'paginate_by', 'ordering']
        context['append_param'] = '&' if any(
            [True for x in pagination_params if x in search_url]) else '?'

        return context

    def get(self, request, *args, **kwargs):
        params = self.get_extra_params(request)
        if params:
            params['filter_params'] = True

        context = self.get_context_data(**params)
        self.object_list = context['object_list']

        if params:
            context.update(params)

        if request.is_ajax():
            paginator = context['paginator']
            more = False
            if paginator.num_pages > 1:
                more = True

            results = [{'id': instance.code, 'text': instance.brand.upper()} for instance in self.object_list]
            data = {
                "results": results,
                "pagination": {
                    "more": more
                }
            }
            return HttpResponse(json.dumps(data))
        return self.render_to_response(context)


class ClientAPIAuthenticatedDetailView(DetailView):
    slug_field = api_client_settings.configs['SLUG_FIELD']
    slug_url_kwarg = api_client_settings.configs['SLUG_FIELD']
    client_method = None

    def get(self, request, *args, **kwargs):
        response = self.client_method(self.kwargs.get(self.slug_field))
        self.object = response.as_obj()
        context = self.get_context_data()
        return self.render_to_response(context)


class ClientAPIAuthenticatedDeleteView(DeleteView):
    slug_field = api_client_settings.configs['SLUG_FIELD']
    slug_url_kwarg = api_client_settings.configs['SLUG_FIELD']
    client_method = None

    def post(self, request, *args, **kwargs):
        self.client_method(self.kwargs.get(self.slug_field))
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)


class ClientAPICreateView(BaseViewMixin, ClientAPIAuthenticatedCreateView):
    pass


class ClientAPIDetailView(BaseViewMixin, ClientAPIAuthenticatedDetailView):
    pass


class ClientAPIUpdateView(BaseViewMixin, ClientAPIAuthenticatedUpdateView):
    pass


class ClientAPIListView(BaseViewMixin, ClientAPIAuthenticatedListView):
    pass


class ClientAPIDeleteView(BaseViewMixin, ClientAPIAuthenticatedDeleteView):
    pass
