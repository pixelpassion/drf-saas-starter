from allauth.account.views import email_verification_sent

from django.conf.urls import url

from .views import GetAllowedVerifyEmailView, TenantRegisterView, TenantUserRegisterView

urlpatterns = [
    url(r'^tenant/$', TenantRegisterView.as_view(), name='tenant_rest_register'),
    url(r'^tenant/(?P<tenant_name>[-:\w]+)/user/$', TenantUserRegisterView.as_view(), name='user_rest_register'),

    # FIXME Do we need this active?
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
    # url(r'^account-confirm-email/(?P<key>[-:\w]+)/$', TemplateView.as_view(),
    #     name='account_confirm_email'),

    url(r'^confirm-email/$', email_verification_sent, name='account_email_verification_sent'),
    url(r'^confirm-email/(?P<key>[-:\w]+)/$', GetAllowedVerifyEmailView.as_view(), name='account_confirm_email'),
]
