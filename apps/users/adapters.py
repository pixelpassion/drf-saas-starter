from allauth.account.adapter import DefaultAccountAdapter
from allauth.utils import get_current_site
from django_saas_email.utils import create_and_send_mail

from django.conf import settings
from django.urls import reverse

from apps.users.models import User


class AccountAdapter(DefaultAccountAdapter):

    def is_open_for_signup(self, request):
        return getattr(settings, 'ACCOUNT_ALLOW_REGISTRATION', True)

    def generate_unique_username(self, txts, regex=None):
        """Use a given username and find the next free ID - if not use the first part of an email."""

        username = txts[3]

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
            'activate_url': context["activate_url"],
            'key': context["key"],
        }

        create_and_send_mail(template_name=template_prefix, context=context_dict, to_address=email)

    def get_email_confirmation_redirect_url(self, request):
        """The URL to return to after successful e-mail confirmation."""

        # TODO: Maybe have a JSON response, when content-type=JSON? Needs to be done higher in the stack

        if settings.EMAIL_VERIFICATION_REDIRECT_URL:
            return settings.EMAIL_VERIFICATION_REDIRECT_URL

        return reverse('email_verified')

    def send_confirmation_mail(self, request, emailconfirmation, signup):

        current_site = get_current_site(request)
        activate_url = self.get_email_confirmation_url(
            request,
            emailconfirmation)
        ctx = {
            "user": emailconfirmation.email_address.user,
            "activate_url": activate_url,
            "current_site": current_site,
            "key": emailconfirmation.key,
        }
        if signup:
            email_template = 'email_confirmation_signup'
        else:
            email_template = 'email_confirmation'

        self.send_mail(email_template, emailconfirmation.email_address.email, ctx)
