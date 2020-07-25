import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import InvalidPage
from django.http import Http404, HttpResponse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, ListView
from django.views.generic.base import ContextMixin
from django.views.generic.edit import FormView
from . import status

from .paginators import ClientAPIPagination
from .utils import clean_url


class PageTitleMixin(ContextMixin):
    page_title = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context


class BaseViewMixin(PageTitleMixin, LoginRequiredMixin):
    pass


class ClientAPIFormMixin(BaseViewMixin, FormView):
    slug_field = 'code'
    slug_url_kwarg = 'code'

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
            return self.form_invalid(form)
        return super().form_valid(form)


class ClientAPIListMixin(BaseViewMixin, ListView):
    http_method_names = ['get']
    paginate_by = 100
    paginator_class = ClientAPIPagination
    client_method = None
    extra_kwargs = []
    page_base_url = ''

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


class ClientAPIDetailMixin(BaseViewMixin, DetailView):
    slug_field = 'code'
    slug_url_kwarg = 'code'
    client_method = None

    def get(self, request, *args, **kwargs):
        response = self.client_method(**self.kwargs)
        instance = response.as_obj()
        self.object = instance
        context = self.get_context_data()
        return self.render_to_response(context)
