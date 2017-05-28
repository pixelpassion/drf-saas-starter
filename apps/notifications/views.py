from __future__ import absolute_import
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views import View

from django_nyt.decorators import json_view

import logging

from django.utils.decorators import method_decorator
from django.shortcuts import render

from django_nyt.utils import notify

logger = logging.getLogger(__name__)

from .forms import NotificationCreateForm



class NotificationCreateView(View):

    form_class = NotificationCreateForm
    initial = {'key': 'value'}
    template_name = 'form_template.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    @method_decorator(json_view)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            instance = self.request.user

            logger.info("New object created: {}, {}".format(form.cleaned_data['name'], str(instance)))

            notify(
                ("Message is: {}".format(form.cleaned_data['name'])),
                "TEST_KEY",
                target_object=instance,
            )

            return {
                'OK': True
            }


class TestLoginAsUser(DetailView):

    model = get_user_model()

    def get(self, *args, **kwargs):
        user = self.get_object()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(self.request, user)
        return redirect('home')