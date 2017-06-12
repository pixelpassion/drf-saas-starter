from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_jwt.settings import api_settings

from django.core import mail
from django.test import override_settings
from django.urls import reverse

from apps.users.tests.factories import UserFactory, VerifiedUserFactory


class APIJWTClient(APIClient):

    def login(self, path, email, password):
        response = self.post(path, {"email": email, "password": password})
        if response.status_code == status.HTTP_200_OK:
            self.credentials(
                HTTP_AUTHORIZATION="{0} {1}".format(api_settings.JWT_AUTH_HEADER_PREFIX, response.data['token'])
            )
            return True
        else:
            return False


@override_settings(LANGUAGE_CODE='en')
class TestLogin(APITestCase):

    def setUp(self):
        self.login_path = reverse('rest_login')
        # Create user and verify him
        self.verified_user = UserFactory(password='test1234')
        VerifiedUserFactory(user=self.verified_user)
        # Create unverified user
        self.unverified_user = UserFactory(password='test1234')
        VerifiedUserFactory(user=self.unverified_user, verified=False)

    def login(self, post_data=None, email=None, password=None):
        if email or password:
            post_data = {"email": email, "password": password}
        response = self.client.post(self.login_path, data=post_data, format='json')
        return response

    def test_successful_login_status(self):
        response = self.login(email=self.verified_user.email, password='test1234')
        assert response.status_code == status.HTTP_200_OK

    def test_successful_login_returns_token(self):
        response = self.login(email=self.verified_user.email, password='test1234')
        assert 'token' in response.data

    def test_successful_login_returns_user_pk(self):
        response = self.login(email=self.verified_user.email, password='test1234')
        assert response.data['user']['pk'] == str(self.verified_user.pk)

    def test_unverified_user_login_status(self):
        response = self.login(email=self.unverified_user.email, password='test1234')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_unverified_user_login_error(self):
        response = self.login(email=self.unverified_user.email, password='test1234')
        assert response.data['error'] == ['E-mail is not verified.']

    def test_unused_email_login_status(self):
        response = self.login(email='unused@test.com', password='test1234')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_unused_email_login_error(self):
        response = self.login(email='unused@test.com', password='test1234')
        assert response.data['error'] == ['Unable to log in with provided credentials.']

    def test_invalid_email_login_status(self):
        response = self.login(email='unused@invalid', password='test1234')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_invalid_email_login_error(self):
        response = self.login(email='unused@invalid', password='test1234')
        assert response.data['email'] == ['Enter a valid email address.']

    def test_empty_email_login_status(self):
        response = self.login(email='', password='test1234')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_empty_email_login_error(self):
        response = self.login(email='', password='test1234')
        assert response.data['error'] == ['Must include "email" and "password".']

    def test_none_email_login_status(self):
        response = self.login(password='test1234')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_none_email_login_error(self):
        response = self.login(password='test1234')
        assert response.data['email'] == ['This field may not be null.']

    def test_missing_email_login_status(self):
        post_data = {"password": "test1234"}
        response = self.login(post_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_missing_email_login_error(self):
        post_data = {"password": "test1234"}
        response = self.login(post_data)
        assert response.data['error'] == ['Must include "email" and "password".']

    def test_wrong_password_login_status(self):
        response = self.login(email=self.verified_user.email, password='wrongpw')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_wrong_password_login_error(self):
        response = self.login(email=self.verified_user.email, password='wrongpw')
        assert response.data['error'] == ['Unable to log in with provided credentials.']

    def test_empty_password_login_status(self):
        response = self.login(email=self.verified_user.email, password='')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_empty_password_login_error(self):
        response = self.login(email=self.verified_user.email, password='')
        assert response.data['password'] == ['This field may not be blank.']

    def test_none_password_login_status(self):
        response = self.login(email=self.verified_user.email)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_none_password_login_error(self):
        response = self.login(email=self.verified_user.email)
        assert response.data['password'] == ['This field may not be null.']

    def test_missing_password_login_status(self):
        post_data = {"email": self.verified_user.email}
        response = self.login(post_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_missing_password_login_error(self):
        post_data = {"email": self.verified_user.email}
        response = self.login(post_data)
        assert response.data['password'] == ['This field is required.']


@override_settings(LANGUAGE_CODE='en')
class TestLogout(APITestCase):
    client_class = APIJWTClient

    def setUp(self):
        self.login_path = reverse('rest_login')
        self.logout_path = reverse('rest_logout')
        self.some_user = UserFactory()
        self.verified_user = UserFactory(password='test1234')
        VerifiedUserFactory(user=self.verified_user)

    def test_forced_login_post_logout_status(self):
        self.client.force_authenticate(user=self.some_user)
        response = self.client.post(self.logout_path)
        assert response.status_code == status.HTTP_200_OK

    def test_forced_login_post_logout_message(self):
        self.client.force_authenticate(user=self.some_user)
        response = self.client.post(self.logout_path)
        assert response.data['detail'] == "Successfully logged out."

    def test_proper_login_post_logout_status(self):
        self.client.login(self.login_path, email=self.verified_user.email, password='test1234')
        response = self.client.post(self.logout_path)
        assert response.status_code == status.HTTP_200_OK

    def test_proper_login_post_logout_message(self):
        self.client.login(self.login_path, email=self.verified_user.email, password='test1234')
        response = self.client.post(self.logout_path)
        assert response.data['detail'] == "Successfully logged out."

    def test_not_logged_in_post_logout_status(self):
        response = self.client.post(self.logout_path)
        assert response.status_code == status.HTTP_200_OK

    def test_not_logged_in_post_logout_message(self):
        response = self.client.post(self.logout_path)
        assert response.data['detail'] == "Successfully logged out."

    def test_forced_login_get_logout_status(self):
        self.client.force_authenticate(user=self.some_user)
        response = self.client.get(self.logout_path)
        assert response.status_code == status.HTTP_200_OK

    def test_forced_login_get_logout_message(self):
        self.client.force_authenticate(user=self.some_user)
        response = self.client.get(self.logout_path)
        assert response.data['detail'] == "Successfully logged out."

    def test_proper_login_get_logout_status(self):
        self.client.login(self.login_path, email=self.verified_user.email, password='test1234')
        response = self.client.get(self.logout_path)
        assert response.status_code == status.HTTP_200_OK

    def test_proper_login_get_logout_message(self):
        self.client.login(self.login_path, email=self.verified_user.email, password='test1234')
        response = self.client.get(self.logout_path)
        assert response.data['detail'] == "Successfully logged out."

    def test_not_logged_in_get_logout_status(self):
        response = self.client.get(self.logout_path)
        assert response.status_code == status.HTTP_200_OK

    def test_not_logged_in_get_logout_message(self):
        response = self.client.get(self.logout_path)
        assert response.data['detail'] == "Successfully logged out."


@override_settings(LANGUAGE_CODE='en')
class TestPasswordChange(APITestCase):
    client_class = APIJWTClient

    def setUp(self):
        self.login_path = reverse('rest_login')
        self.password_change_path = reverse('rest_password_change')
        self.verified_user = UserFactory(password='test1234')
        VerifiedUserFactory(user=self.verified_user)
        self.client.login(self.login_path, email=self.verified_user.email, password='test1234')

    def change_password(self, post_data=None, new_password1=None, new_password2=None):
        if new_password1 or new_password1:
            post_data = {"new_password1": new_password1, "new_password2": new_password2}
        response = self.client.post(self.password_change_path, data=post_data, format='json')
        return response

    def test_change_password_status(self):
        response = self.change_password(new_password1='new56789', new_password2='new56789')
        assert response.status_code == status.HTTP_200_OK

    def test_change_password_message(self):
        response = self.change_password(new_password1='new56789', new_password2='new56789')
        assert 'detail' in response.data  # FIXME Because of some translation issue I can't access the content

    def test_new_password_login(self):
        self.change_password(new_password1='new56789', new_password2='new56789')
        self.client.logout()
        assert self.client.login(self.login_path, email=self.verified_user.email, password='new56789')

    def test_old_password_login(self):
        self.change_password(new_password1='new56789', new_password2='new56789')
        self.client.logout()
        assert self.client.login(self.login_path, email=self.verified_user.email, password='test1234') == False

    def test_short_password_change_status(self):
        response = self.change_password(new_password1='short', new_password2='short')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_short_password_change_error(self):
        response = self.change_password(new_password1='short', new_password2='short')
        assert response.data['new_password2'] == ['This password is too short. It must contain at least 8 characters.']

    def test_empty_password_status(self):
        post_data = {"new_password1": "", "new_password2": ""}
        response = self.change_password(post_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_empty_password_error(self):
        post_data = {"new_password1": "", "new_password2": ""}
        response = self.change_password(post_data)
        assert response.data['new_password1'] == ['This field may not be blank.']
        assert response.data['new_password2'] == ['This field may not be blank.']

    def test_none_password_status(self):
        post_data = {"new_password1": None, "new_password2": None}
        response = self.change_password(post_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_none_password_error(self):
        post_data = {"new_password1": None, "new_password2": None}
        response = self.change_password(post_data)
        assert response.data['new_password1'] == ['This field may not be null.']
        assert response.data['new_password2'] == ['This field may not be null.']

    def test_old_password_change_status(self):
        response = self.change_password(new_password1='test1234', new_password2='test1234')
        assert response.status_code == status.HTTP_200_OK

    def test_old_password_change_message(self):
        response = self.change_password(new_password1='test1234', new_password2='test1234')
        assert 'detail' in response.data  # FIXME Because of some translation issue I can't access the content

    def test_different_passwords_status(self):
        response = self.change_password(new_password1='new56789', new_password2='diff7654')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_different_passwords_error(self):
        response = self.change_password(new_password1='new56789', new_password2='diff7654')
        assert response.data['new_password2'] == ["The two password fields didn't match."]

    def test_no_new_password1_status(self):
        post_data = {"new_password2": "new56789"}
        response = self.change_password(post_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_no_new_password1_error(self):
        post_data = {"new_password2": "new56789"}
        response = self.change_password(post_data)
        assert response.data['new_password1'] == ['This field is required.']

    def test_no_new_password2_status(self):
        post_data = {"new_password1": "new56789"}
        response = self.change_password(post_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_no_new_password2_error(self):
        post_data = {"new_password1": "new56789"}
        response = self.change_password(post_data)
        assert response.data['new_password2'] == ['This field is required.']

    def test_empty_post_data_status(self):
        post_data = {}
        response = self.change_password(post_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_empty_post_data_error(self):
        post_data = {}
        response = self.change_password(post_data)
        assert response.data['new_password1'] == ['This field is required.']
        assert response.data['new_password2'] == ['This field is required.']

    def test_none_post_data_status(self):
        response = self.change_password()
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_none_post_data_error(self):
        response = self.change_password()
        assert response.data['new_password1'] == ['This field is required.']
        assert response.data['new_password2'] == ['This field is required.']


@override_settings(LANGUAGE_CODE='en')
class TestPasswordResetInitiate(APITestCase):

    def setUp(self):
        self.password_reset_path = reverse('rest_password_reset')
        self.verified_user = UserFactory()
        VerifiedUserFactory(user=self.verified_user)

    def test_password_reset_status(self):
        response = self.client.post(self.password_reset_path, data={"email": self.verified_user.email})
        assert response.status_code == status.HTTP_200_OK

    def test_password_reset_message(self):
        response = self.client.post(self.password_reset_path, data={"email": self.verified_user.email})
        assert str(response.data['detail']) == 'Password reset e-mail has been sent.'

    def test_password_reset_email_sent(self):
        response = self.client.post(self.password_reset_path, data={"email": self.verified_user.email})
        assert len(mail.outbox) == 1

    def test_password_reset_email_subject(self):
        response = self.client.post(self.password_reset_path, data={"email": self.verified_user.email})
        assert mail.outbox[0].subject == 'Password reset on example.com'

    def test_password_reset_unregistered_email_status(self):
        response = self.client.post(self.password_reset_path, data={"email": "unregistered@test.com"})
        assert response.status_code == status.HTTP_200_OK

    def test_password_reset_unregistered_email_message(self):
        response = self.client.post(self.password_reset_path, data={"email": "unregistered@test.com"})
        assert str(response.data['detail']) == 'Password reset e-mail has been sent.'

    def test_password_reset_unregistered_email_not_sent(self):
        response = self.client.post(self.password_reset_path, data={"email": "unregistered@test.com"})
        assert len(mail.outbox) == 0

    def test_empty_password_reset_status(self):
        response = self.client.post(self.password_reset_path, data={})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_empty_password_reset_message(self):
        response = self.client.post(self.password_reset_path, data={})
        assert response.data['email'] == ['This field is required.']

    def test_empty_email_password_reset_status(self):
        response = self.client.post(self.password_reset_path, data={"email": ""})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_empty_email_password_reset_message(self):
        response = self.client.post(self.password_reset_path, data={"email": ""})
        assert response.data['email'] == ['This field may not be blank.']

    def test_none_email_password_reset_status(self):
        response = self.client.post(self.password_reset_path, data={"email": None})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_none_email_password_reset_message(self):
        response = self.client.post(self.password_reset_path, data={"email": None})
        assert response.data['email'] == ['Enter a valid email address.']
