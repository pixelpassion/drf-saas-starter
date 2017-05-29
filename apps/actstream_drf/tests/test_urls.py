from django.test import TestCase
from django.urls import resolve, reverse

from apps.users.tests.factories import UserFactory


class TestURLs(TestCase):
    """Test whether the the URLs for activities of users can be resolved and reversed.

    This only works if the integration with user has been made.
    """

    def setUp(self):
        self.user_pk = UserFactory().pk

    def test_activities_reverse(self):
        assert reverse('users:user-activities', kwargs={'pk': self.user_pk}) == f'/api/users/{self.user_pk}/activities/'

    def test_activities_resolve(self):
        assert resolve(f'/api/users/{self.user_pk}/activities/').view_name == 'users:user-activities'
