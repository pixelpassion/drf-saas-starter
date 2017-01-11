# -*- coding: utf-8 -*-
from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from allauth.utils import get_user_model
from allauth.account.utils import user_field
from allauth import app_settings

#from metronom.base.celery import send_anymail_mail



class AccountAdapter(DefaultAccountAdapter):

    def is_open_for_signup(self, request):
        return getattr(settings, 'ACCOUNT_ALLOW_REGISTRATION', True)

    def generate_unique_username(self, txts, regex=None):#
        print("generate_unique_username is running")
        print(txts)

            if username is None or username == '':
                username = User.objects.find_next_available_username(email.split("@")[0])
        return super(AccountAdapter, self).generate_unique_username(txts, regex)

    def save_user(self, request, user, form, commit=True):
        """
        Saves a new `User` instance using information provided in the
        signup form.
        """
        from allauth.account.utils import user_username, user_email, user_field

        data = form.cleaned_data
        print(data)

        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        username = data.get('username')
        user_email(user, email)
        user_username(user, username)
        if first_name:
            user_field(user, 'first_name', first_name)
        if last_name:
            user_field(user, 'last_name', last_name)
        if 'password1' in data:
            user.set_password(data["password1"])
        else:
            user.set_unusable_password()

        self.populate_username(request, user)

        print(user.username)

        if commit:
            # Ability not to commit makes it easier to derive from
            # this adapter by adding
            user.save()
        return user

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
