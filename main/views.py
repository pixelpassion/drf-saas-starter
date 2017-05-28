from django.contrib.auth import get_user_model
from django.views.generic.base import TemplateView


from django_nyt.forms import SettingsForm
from django_nyt.models import Notification, Settings

from apps.notifications.forms import NotificationCreateForm
from django.core.cache import cache


class HomeView(TemplateView):

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        c = TemplateView.get_context_data(self, **kwargs)
        user_model = get_user_model()
        c['users'] = user_model.objects.all()
        if self.request.user.is_authenticated():
            c['notifications'] = Notification.objects.filter(
                user=self.request.user
            ).order_by(
                '-created'
            )
            c['settings_form'] = SettingsForm(
                instance=Settings.get_default_setting(self.request.user)
            )
            c['testmodel_form'] = NotificationCreateForm()

        c['ws_messages'] = cache.get("ws_messages")

        return c