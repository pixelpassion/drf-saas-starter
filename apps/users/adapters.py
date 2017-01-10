# -*- coding: utf-8 -*-
from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings

#from metronom.base.celery import send_anymail_mail


class AccountAdapter(DefaultAccountAdapter):

    def is_open_for_signup(self, request):
        return getattr(settings, 'ACCOUNT_ALLOW_REGISTRATION', True)

    def send_mail(self, template_prefix, email, context):

        context_dict = {
            'template_prefix': template_prefix,
            'email': email,
            'current_site': context["current_site"].id,
            'activate_url':  context["activate_url"],
            'key':  context["key"],
            'user':  context["user"].id
        }

        print("mail was send")

        #send_anymail_mail.delay(context_dict)
