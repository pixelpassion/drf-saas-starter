from django.test import TestCase
from django.urls import resolve, reverse

from apps.users.tests.factories import UserFactory


class TestURLs(TestCase):
    """Test whether the the URLs for comments on users can be resolved and reversed.

    This only works if the integration with user has been made.
    """

    def setUp(self):
        self.user_pk = UserFactory().pk

    def test_comments_reverse(self):
        assert reverse('users:user-comments', kwargs={'pk': self.user_pk}) == f'/api/users/{self.user_pk}/comments/'

    def test_comments_resolve(self):
        assert resolve(f'/api/users/{self.user_pk}/comments/').view_name == 'users:user-comments'
