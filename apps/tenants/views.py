from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView

from apps.tenants.mixins import TenantAccessRequiredMixin


class TenantDashboardView(LoginRequiredMixin, TenantAccessRequiredMixin, TemplateView):
    """ A tenant dashboard - just for testing, because all the logic should be in the frontend"""
    template_name = "tenants/dashboard.html"
