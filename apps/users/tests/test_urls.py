from django.test import TestCase
from django.urls import resolve, reverse

from apps.users.tests.factories import UserFactory


class TestUsersURLs(TestCase):

    def setUp(self):
        self.user = UserFactory()

    def test_user_list_reverse(self):
        reverse('users:user-list') == '/api/users/'

    def test_user_list_resolve(self):
        assert resolve('/api/users/').view_name == 'users:user-list'

    def test_user_detail_reverse(self):
        reverse('users:user-detail', kwargs={'pk': self.user.pk}) == f'/api/users/{self.user.pk}/'

    def test_user_detail_resolve(self):
        resolve(f'/api/users/{self.user.pk}/').view_name == 'users:user-detail'
