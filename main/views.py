from django.views.generic.base import TemplateView

from django.core.cache import cache


class HomeView(TemplateView):

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        context['ws_messages'] = cache.get("ws_messages")

        return context