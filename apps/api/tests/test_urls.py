from django.test import TestCase
from django.urls import resolve, reverse


class TestAPIURLs(TestCase):

    def test_api_rest_password_reset_reverse(self):
        assert reverse('rest_password_reset') == '/api/password/reset/'

    def test_api_rest_password_reset_resolve(self):
        assert resolve('/api/password/reset/').view_name == 'rest_password_reset'

    def test_api_rest_password_reset_confirm_reverse(self):
        assert reverse('rest_password_reset_confirm') == '/api/password/reset/confirm/'

    def test_api_rest_password_reset_confirm_resolve(self):
        assert resolve('/api/password/reset/confirm/').view_name == 'rest_password_reset_confirm'

    def test_api_rest_login_reverse(self):
        assert reverse('rest_login') == '/api/login/'

    def test_api_rest_login_resolve(self):
        assert resolve('/api/login/').view_name == 'rest_login'

    def test_api_rest_logout_reverse(self):
        assert reverse('rest_logout') == '/api/logout/'

    def test_api_rest_logout_resolve(self):
        assert resolve('/api/logout/').view_name == 'rest_logout'

    def test_api_rest_user_details_reverse(self):
        assert reverse('rest_user_details') == '/api/current-user/'

    def test_api_rest_user_details_resolve(self):
        assert resolve('/api/current-user/').view_name == 'rest_user_details'

    def test_api_docs_reverse(self):
        assert reverse('api_docs') == '/api/docs/'

    def test_api_docs_resolve(self):
        assert resolve('/api/docs/').view_name == 'api_docs'
