from django.test import TestCase
from django.urls import resolve, reverse


class TestMainURLs(TestCase):

    def test_home_reverse(self):
        assert reverse('home') == '/'

    def test_home_resolve(self):
        assert resolve('/').view_name == 'home'

    def test_email_verified_reverse(self):
        assert reverse('email_verified') == '/email-verified/'

    def test_email_verified_resolve(self):
        assert resolve('/email-verified/').view_name == 'email_verified'

    def test_password_reset_confirm_reverse(self):
        pass

    def test_passwort_reset_confirm_resolve(self):
        pass
