from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse

from apps.comments.tests.factories import CommentUserFactory
from apps.users.tests.factories import UserFactory


class TestGetActivities(APITestCase):

    def setUp(self):
        self.commented_user = UserFactory()
        self.comment = CommentUserFactory(content_object=self.commented_user)
        self.endpoint = reverse('users:user-activities', kwargs={'pk': self.commented_user.pk})
        self.reading_user = UserFactory()
        self.client.force_authenticate(user=self.reading_user)
        self.response = self.client.get(self.endpoint)

    def test_get_activities_should_return_ok_status(self):
        assert self.response.status_code == status.HTTP_200_OK

    def test_result_should_contain_right_actor(self):
        assert self.response.data['results'][0]['actor']['id'] == str(self.comment.author.pk)

    def test_result_should_contain_right_verb(self):
        assert self.response.data['results'][0]['verb'] == 'made comment'

    def test_result_should_contain_action_object_with_right_content(self):
        assert self.response.data['results'][0]['action_object']['content'] == self.comment.content

    def test_result_should_contain_right_target(self):
        assert self.response.data['results'][0]['target']['id'] == str(self.commented_user.pk)

    def test_result_should_contain_timestamp(self):
        assert 'timestamp' in self.response.data['results'][0]


class TestGetUnauthorizedActivities(APITestCase):

    def setUp(self):
        self.commented_user = UserFactory()
        self.comment = CommentUserFactory(content_object=self.commented_user)
        self.endpoint = reverse('users:user-activities', kwargs={'pk': self.commented_user.pk})
        self.response = self.client.get(self.endpoint)

    def test_get_activities_should_return_unauthorized_status(self):
        assert self.response.status_code == status.HTTP_401_UNAUTHORIZED
