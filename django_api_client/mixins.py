from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import ContextMixin


class PageTitleMixin(ContextMixin):
    page_title = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context


class BaseViewMixin(PageTitleMixin, LoginRequiredMixin):
    pass
