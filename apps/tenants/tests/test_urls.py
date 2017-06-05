from django.test import TestCase
from django.urls import resolve, reverse

from apps.tenants.tests.factories import TenantFactory


class TestTenantsURLs(TestCase):

    def setUp(self):
        self.tenant = TenantFactory()

    def test_tenants_dashboard_reverse(self):
        assert reverse('tenants:dashboard') == '/tenant/dashboard/'

    def test_tenants_dashboard_resolve(self):
        assert resolve('/tenant/dashboard/').view_name == 'tenants:dashboard'

    def test_tenants_registration_rest_register_reverse(self):
        assert reverse('tenant_rest_register') == '/api/sign-up/tenant/'

    def test_tenants_registration_rest_register_resolve(self):
        assert resolve('/api/sign-up/tenant/').view_name == 'tenant_rest_register'

    def test_tenants_registration_user_rest_register_reverse(self):
        kwargs = {'tenant_name': self.tenant.name}
        assert reverse('user_rest_register', kwargs=kwargs) == f'/api/sign-up/tenant/{self.tenant.name}/user/'

    def test_tenants_registration_user_rest_register_resolve(self):
        assert resolve(f'/api/sign-up/tenant/{self.tenant.name}/user/').view_name == 'user_rest_register'

    def test_tenants_registration_email_verification_sent_reverse(self):
        assert reverse('account_email_verification_sent') == '/api/sign-up/confirm-email/'

    def test_tenants_registration_email_verification_sent_resolve(self):
        assert resolve('/api/sign-up/confirm-email/').view_name == 'account_email_verification_sent'

    def test_tenants_registration_account_confirm_email_reverse(self):
        pass

    def test_tenants_registration_account_confirm_email_resolve(self):
        pass
