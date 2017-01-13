# -*- coding: utf-8 -*-
from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from allauth.utils import get_user_model
from allauth.account.utils import user_field
from allauth import app_settings

from apps.users.models import User

#from metronom.base.celery import send_anymail_mail


class AccountAdapter(DefaultAccountAdapter):

    def is_open_for_signup(self, request):
        return getattr(settings, 'ACCOUNT_ALLOW_REGISTRATION', True)

    def generate_unique_username(self, txts, regex=None):
        """Use a given username and find the next free ID - if not use the first part of an email """

        username=txts[3]

        if username is None or username == '':
            email = txts[2]
            return User.objects.find_next_available_username(email.split("@")[0])
        else:
            return User.objects.find_next_available_username(username)

    def send_mail(self, template_prefix, email, context):

        context_dict = {
            'template_prefix': template_prefix,
            'email': email,
            'current_site': context["current_site"].id,
            'activate_url':  context["activate_url"],
            'key':  context["key"],
            'user':  context["user"].id
        }

        print("mail was send with {}".format(context_dict))

        #send_anymail_mail.delay(context_dict)
