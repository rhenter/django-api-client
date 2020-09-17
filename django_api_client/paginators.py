import inspect
from math import ceil

from django.core.paginator import EmptyPage, Page, PageNotAnInteger
from django.utils.functional import cached_property
from django.utils.inspect import method_has_no_args
from django.utils.translation import gettext_lazy as _


class ClientAPIPagination:
    def __init__(self, client_method, per_page, **kwargs):
        params =  kwargs.get('extra_params', {})
        params.update({
            'limit': per_page,
            'offset': 0
        })

        self.extra_params = params
        self.client_method = client_method

        self.object_list = client_method(params=self.extra_params).as_obj()
        self.per_page = int(per_page)

    @cached_property
    def count(self):
        """Return the total number of objects, across all pages."""
        c = getattr(self.object_list, 'count', None)
        if callable(c) and not inspect.isbuiltin(c) and method_has_no_args(c):
            return c()
        return self.object_list.count

    @cached_property
    def num_pages(self):
        """Return the total number of pages."""
        if self.count == 0:
            return 0
        hits = max(1, self.count)
        return ceil(hits / self.per_page)

    @property
    def page_range(self):
        """
        Return a 1-based range of pages for iterating through within
        a template for loop.
        """
        return range(1, self.num_pages + 1)

    def validate_number(self, number):
        """Validate the given 1-based page number."""
        try:
            if isinstance(number, float) and not number.is_integer():
                raise ValueError
            number = int(number)
        except (TypeError, ValueError):
            raise PageNotAnInteger(_('That page number is not an integer'))
        if number < 1:
            raise EmptyPage(_('That page number is less than 1'))
        if number > self.num_pages:
            if number == 1:
                pass
            else:
                raise EmptyPage(_('That page contains no results'))
        return number

    def get_page(self, number):
        """
        Return a valid page, even if the page argument isn't a number or isn't
        in range.
        """
        try:
            number = self.validate_number(number)
        except PageNotAnInteger:
            number = 1
        except EmptyPage:
            number = self.num_pages
        return self.page(number)

    def page(self, number):
        """Return a Page object for the given 1-based page number."""
        number = self.validate_number(number)
        offset = (number - 1) * self.per_page
        limit = self.per_page

        params = {
            'limit': limit,
            'offset': offset
        }
        if offset != 0:
            self.extra_params.update(params)
            object_list = self.client_method(params=self.extra_params).as_obj()
        else:
            object_list = self.object_list
        return self._get_page(object_list.results, number, self)

    def _get_page(self, *args, **kwargs):
        """
        Return an instance of a single page.

        This hook can be used by subclasses to use an alternative to the
        standard :cls:`Page` object.
        """
        return Page(*args, **kwargs)
