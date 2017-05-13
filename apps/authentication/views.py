from allauth import app_settings
from allauth.account import app_settings
from allauth.account.forms import LoginForm
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC
from allauth.account.utils import get_next_redirect_url, passthrough_next_redirect_url
from allauth.account.views import ConfirmEmailView as AllAuthConfirmEmailView
from allauth.account.views import AjaxCapableProcessFormViewMixin, \
    RedirectAuthenticatedUserMixin, sensitive_post_parameters_m
from allauth.compat import reverse
from allauth.exceptions import ImmediateHttpResponse
from allauth.utils import get_current_site, get_form_class, get_request_param
from main.logging import logger
from rest_auth.registration.serializers import VerifyEmailSerializer
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.edit import FormView

from .serializers import VerifyEmailSerializer

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters('password')
)


class LoginView(RedirectAuthenticatedUserMixin,
                AjaxCapableProcessFormViewMixin,
                FormView):
    form_class = LoginForm
    template_name = "account/login." + app_settings.TEMPLATE_EXTENSION
    success_url = None
    redirect_field_name = "next"

    @sensitive_post_parameters_m
    def dispatch(self, request, *args, **kwargs):
        print("WE ARE IN")
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(LoginView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_form_class(self):
        return get_form_class(app_settings.FORMS, 'login', self.form_class)

    def form_valid(self, form):
        success_url = self.get_success_url()
        try:
            return form.login(self.request, redirect_url=success_url)
        except ImmediateHttpResponse as e:
            return e.response

    def get_success_url(self):
        # Explicitly passed ?next= URL takes precedence
        ret = (get_next_redirect_url(
            self.request,
            self.redirect_field_name) or self.success_url)
        print("gsi: {}".format(ret))
        return ret

    def get_context_data(self, **kwargs):
        ret = super(LoginView, self).get_context_data(**kwargs)
        signup_url = passthrough_next_redirect_url(self.request,
                                                   reverse("account_signup"),
                                                   self.redirect_field_name)
        redirect_field_value = get_request_param(self.request,
                                                 self.redirect_field_name)
        site = get_current_site(self.request)

        ret.update({"signup_url": signup_url,
                    "site": site,
                    "redirect_field_name": self.redirect_field_name,
                    "redirect_field_value": redirect_field_value})
        return ret


login = LoginView.as_view()


class ConfirmEmailView(APIView, AllAuthConfirmEmailView):
    permission_classes = (AllowAny,)
    allowed_methods = ('GET', 'OPTIONS', 'HEAD')

    def get_serializer(self, *args, **kwargs):
        return VerifyEmailSerializer(*args, **kwargs)

    def get(self, *args, **kwargs):

        logger.warning("GET")

        self.object = confirmation = self.get_object()

        if confirmation.email_address.user != self.request.user and self.request.user.is_authenticated():
            messages.add_message(self.request._request, messages.ERROR, 'You can not verify this email address, you must logout first!')
            return redirect("/")

        confirmation.confirm(self.request)

        # User gets activated
        user = confirmation.email_address.user
        user.is_active = True
        user.save()

        messages.add_message(self.request._request, messages.SUCCESS, 'Thanks for verifiying your email address, you can login now')

        tenant = user.tenants.all()[0]

        # TODO: Invalidate the key

        # Get the redirect URL
        redirect_url = self.get_redirect_url()

        if not redirect_url:
            ctx = self.get_context_data()
            return self.render_to_response(ctx)

        tenant_redirect_url = "{}{}".format(tenant.domain, redirect_url)
        return redirect(tenant_redirect_url)

    def get_object(self, queryset=None):
        key = self.kwargs['key']
        emailconfirmation = EmailConfirmationHMAC.from_key(key)
        if not emailconfirmation:
            if queryset is None:
                queryset = self.get_queryset()
            try:
                emailconfirmation = queryset.get(key=key.lower())
            except EmailConfirmation.DoesNotExist:
                raise Http404()
        return emailconfirmation
