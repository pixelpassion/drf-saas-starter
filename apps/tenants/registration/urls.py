from django.views.generic import TemplateView
from django.conf.urls import url

from rest_auth.registration.views import VerifyEmailView, RegisterView
from .views import TenantUserRegisterView

urlpatterns = [
    url(r'^tenant$', RegisterView.as_view(), name='tenant_rest_register'),
    url(r'^tenant/(?P<tenant_name>[-:\w]+)/user$', TenantUserRegisterView.as_view(), name='user_rest_register'),
    url(r'^verify-email/$', VerifyEmailView.as_view(), name='rest_verify_email'),

    # This url is used by django-allauth and empty TemplateView is
    # defined just to allow reverse() call inside app, for example when email
    # with verification link is being sent, then it's required to render email
    # content.

    # account_confirm_email - You should override this view to handle it in
    # your API client somehow and then, send post to /verify-email/ endpoint
    # with proper key.
    # If you don't want to use API on that step, then just use ConfirmEmailView
    # view from:
    # django-allauth https://github.com/pennersr/django-allauth/blob/master/allauth/account/views.py
    url(r'^account-confirm-email/(?P<key>[-:\w]+)/$', TemplateView.as_view(),
        name='account_confirm_email'),
]