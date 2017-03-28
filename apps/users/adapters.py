# -*- coding: utf-8 -*-
from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings

from apps.users.models import User
from apps.mails.utils import create_and_send_mail


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
            'email': email,
            'site_domain': context["current_site"].domain,
            'site_name': context["current_site"].name,
            'activate_url':  context["activate_url"],
            'key':  context["key"],
        }

        create_and_send_mail(template=template_prefix, context=context_dict, to_address=email)

    def get_email_confirmation_redirect_url(self, request):
        """ The URL to return to after successful e-mail confirmation. """

        return settings.EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL
