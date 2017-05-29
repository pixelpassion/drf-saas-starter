from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from apps.comments.models import Comment
from apps.comments.tests.factories import CommentUserFactory
from apps.users.tests.factories import UserFactory


class TestPostCorrectComment(APITestCase):

    def setUp(self):
        self.commenter = UserFactory()
        self.commented_user = UserFactory()
        self.post_data = {"content": "This is a comment on a User."}
        self.endpoint = reverse('users:user-comments', kwargs={'pk': self.commented_user.pk})
        self.client.force_authenticate(user=self.commenter)
        self.response = self.client.post(self.endpoint, self.post_data)

    def test_post_correct_comment_should_return_created_status(self):
        assert self.response.status_code == status.HTTP_201_CREATED

    def test_post_correct_comment_should_return_posted_content(self):
        assert self.response.data['content'] == self.post_data['content']

    def test_post_correct_comment_should_return_commenter_as_author(self):
        assert self.response.data['author'] == self.commenter.pk

    def test_post_correct_comment_should_return_correct_object_id_of_commented_object(self):
        assert self.response.data['object_id'] == str(self.commented_user.pk)

    def test_post_correct_comment_should_return_correct_content_type_of_commented_object(self):
        content_type = ContentType.objects.get_for_model(self.commented_user)
        assert self.response.data['content_type'] == content_type.pk


class TestPostIncorrectComment(APITestCase):

    def setUp(self):
        self.commenter = UserFactory()
        self.commented_user = UserFactory()
        self.endpoint = reverse('users:user-comments', kwargs={'pk': self.commented_user.pk})
        self.client.force_authenticate(user=self.commenter)

    def test_post_empty_data_should_return_bad_request(self):
        post_data = None
        response = self.client.post(self.endpoint, post_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_add_different_author_manually_should_be_ignored(self):
        different_author = UserFactory()
        post_data = {
            "content": "This is a comment on a User.",
            "author": different_author.pk
        }
        response = self.client.post(self.endpoint, post_data)
        assert response.data['author'] == self.commenter.pk

    def test_add_different_object_id_manually_should_be_ignored(self):
        different_commented_user = UserFactory()
        post_data = {
            "content": "This is a comment on a User.",
            "object_id": different_commented_user.pk
        }
        response = self.client.post(self.endpoint, post_data)
        assert response.data['object_id'] == str(self.commented_user.pk)

    def test_add_different_content_type_manually_should_be_ignored(self):
        different_content_type = ContentType.objects.get_for_model(Comment)
        post_data = {
            "content": "This is a comment on a User.",
            "content_type": different_content_type.pk
        }
        response = self.client.post(self.endpoint, post_data)
        content_type = ContentType.objects.get_for_model(self.commented_user)
        assert response.data['content_type'] == content_type.pk


class TestPostUnauthorizedComment(APITestCase):

    def setUp(self):
        self.commented_user = UserFactory()
        self.post_data = {"content": "This is a comment on a User."}
        self.endpoint = reverse('users:user-comments', kwargs={'pk': self.commented_user.pk})
        self.response = self.client.post(self.endpoint, self.post_data)

    def test_post_unauthorized_correct_comment_should_return_unauthorized_status(self):
        assert self.response.status_code == status.HTTP_401_UNAUTHORIZED


class TestGetComments(APITestCase):

    def setUp(self):
        self.commented_user = UserFactory()
        self.comment1 = CommentUserFactory(content_object=self.commented_user)
        self.comment2 = CommentUserFactory(content_object=self.commented_user)
        self.comment3 = CommentUserFactory(content_object=self.commented_user)
        self.endpoint = reverse('users:user-comments', kwargs={'pk': self.commented_user.pk})
        self.reading_user = UserFactory()
        self.client.force_authenticate(user=self.reading_user)
        self.response = self.client.get(self.endpoint)

    def test_get_comments_should_return_ok_status(self):
        assert self.response.status_code == status.HTTP_200_OK

    def test_first_result_should_contain_content_of_first_comment(self):
        assert self.response.data['results'][0]['content'] == self.comment1.content

    def test_last_result_should_contain_content_of_last_comment(self):
        assert self.response.data['results'][-1]['content'] == self.comment3.content

    def test_result_should_contain_right_author(self):
        assert self.response.data['results'][0]['author'] == self.comment1.author.pk

    def test_result_should_contain_right_object_id(self):
        assert self.response.data['results'][0]['object_id'] == str(self.commented_user.pk)

    def test_result_should_contain_right_content_type(self):
        assert self.response.data['results'][0]['content_type'] == self.comment1.content_type.pk

    def test_result_should_contain_time_created(self):
        assert 'time_created' in self.response.data['results'][0]


class TestGetUnauthorizedComments(APITestCase):

    def setUp(self):
        self.commented_user = UserFactory()
        self.comment1 = CommentUserFactory(content_object=self.commented_user)
        self.comment2 = CommentUserFactory(content_object=self.commented_user)
        self.comment3 = CommentUserFactory(content_object=self.commented_user)
        self.endpoint = reverse('users:user-comments', kwargs={'pk': self.commented_user.pk})
        self.response = self.client.get(self.endpoint)

    def test_get_unauthorized_comments_should_return_unauthorized_status(self):
        assert self.response.status_code == status.HTTP_401_UNAUTHORIZED
