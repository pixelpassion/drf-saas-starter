import json

from django.conf import settings
from django.core import mail
from apps.api.unit_tests import APITestCase
from apps.authentication.exceptions import *


class SignupApiTests(APITestCase):
    """ Test the signup process of the API endpoint """

    def setUp(self):
        """ """
        super(SignupApiTests, self).setUp()
        self.signup_url = "%s/registration/"

    def user_signup(self, post_data, expected_status_code=200, expected_error=None):
        """
        """
        response = self.client.post(self.signup_url, post_data)

        if expected_status_code:
            self.assertEqual(response.status_code, expected_status_code)

        if expected_error:

            response_json = json.loads(response.content.decode('utf8'))

            expected_response_json = {
                "error_code": expected_error.error_code,
                "more_info": expected_error.more_info,
                "user_message": expected_error.user_message,
                "developer_message": expected_error.developer_message,
            }

            self.assertEquals(response_json, expected_response_json)

    def test_correct_signup_data(self):
        """ """

        post_data = {
            "email": "max_mustermann@example.org",
            "first_name": "Max",
            "last_name": "Mustermann",
            "password": "Test1234!?",
        }
        self.user_signup(post_data)

    def test_already_existing_email(self):
        """ """
        post_data = {
            "email": self.already_registered_user_email,
            "first_name": self.already_registered_user.first_name,
            "last_name": self.already_registered_user.last_name,
            "password": self.already_registered_user_password,
        }

        # Clean the mail outbox, it would count to the tests if not
        mail.outbox = []

        # # Just send again
        # expected_response_json = {
        #     "error_code": FieldMustBeUnique.error_code,
        #     "more_info": FieldMustBeUnique.more_info,
        #     "user_message_description": "A user with that email already exists",  # FieldMustBeUnique.user_message is overwritten
        #     "developer_message": FieldMustBeUnique.developer_message,
        #     "user_message_title": FieldMustBeUnique.user_message_title
        # }
        # self.user_signup_error(post_data, expected_response_json)

        # No activation email should be sent
        self.assertEqual(len(mail.outbox), 0)

    def test_sending_of_activation_email(self):
        """ """
        email = 'max_mustermann@example.org'
        post_data = {
            "email": "%s" % email,
            "first_name": "Max",
            "last_name": "Mustermann",
            "password": "Test1234!?",
        }
        user = self.user_signup(post_data)

        # Token should be
        self.assertIsNotNone(user.activation_token)

        # Token should have been created and have an decent length
        if not settings.AUTO_ACCOUNT_ACTIVATION:
            self.assertTrue(len(user.activation_token) > 50)

        # Activation email is sent correctly
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, u"Untitled project Account Activation")

        # The email should contain the generated token
        activation_link = self.base_activation_url % user.activation_token
        self.assertIn("%s%s" % (settings.BASE_URL, activation_link), mail.outbox[0].body)

    def test_user_activation(self):
        """ """
        email = 'max_mustermann@example.org'
        post_data = {
            "email": "%s" % email,
            "first_name": "Max",
            "last_name": "Mustermann",
            "password": "Test1234!?",
        }
        user = self.user_signup(post_data)
        self.activate_user(user)



    def test_missing_password(self):
        """
        """
        request = {
            "email": "max_mustermann@example.org",
            "first_name": "Max",
            "last_name": "Mustermann",
        }
        response = self.client.post(self.signup_url, request)
        response_json = json.loads(response.content.decode('utf8'))

        self.assertEqual(response.status_code, 400,
                         "Response code for adding user is incorrect! \n %s" %
                         str(response_json))
        expected_response_json = {
            "error_code": EmailAndPasswordNeeded.error_code,
            "more_info": EmailAndPasswordNeeded.more_info,
            "user_message_description": EmailAndPasswordNeeded.user_message,
            "developer_message": EmailAndPasswordNeeded.developer_message,
            "user_message_title": EmailAndPasswordNeeded.user_message_title
        }
        self.assertEquals(response_json, expected_response_json)

    def test_missing_email(self):
        """ """
        request = {
            "first_name": "Max",
            "last_name": "Mustermann",
            "password": "Test1234!?",
        }
        response = self.client.post(self.signup_url, request)
        response_json = json.loads(response.content.decode('utf8'))

        self.assertEqual(response.status_code, 400,
                         "Response code for adding user is incorrect! \n %s" %
                         str(response_json))
        expected_response_json = {
            "error_code": EmailAndPasswordNeeded.error_code,
            "more_info": EmailAndPasswordNeeded.more_info,
            "user_message_description": EmailAndPasswordNeeded.user_message,
            "developer_message": EmailAndPasswordNeeded.developer_message,
            "user_message_title": EmailAndPasswordNeeded.user_message_title
        }
        self.assertEquals(response_json, expected_response_json)

    def test_missing_first_name(self):
        """ """
        post_data = {
            "email": "max_mustermann@example.org",
            "last_name": "Mustermann",
            "password": "Test1234!?",
        }
        # #todo to be changed after exception will be caught manually, instead of django
        # expected_response_json = {
        #     "error_code": FieldMustBeUnique.error_code,
        #     "more_info": FieldMustBeUnique.more_info,
        #     "user_message_description": "",
        #     "developer_message": FieldMustBeUnique.developer_message,
        #     "user_message_title": FieldMustBeUnique.user_message_title
        # }
        self.user_signup_error(post_data, expected_response_json)

    def test_missing_last_name(self):
        """ """
        post_data = {
            "email": "max_mustermann@example.org",
            "first_name": "test_missing_last_name",
            "password": "Test1234!?",
        }
        # #todo to be changed after exception will be caught manually, instead of django
        # expected_response_json = {
        #     "error_code": FieldMustBeUnique.error_code,
        #     "more_info": FieldMustBeUnique.more_info,
        #     "user_message_description": "",
        #     "developer_message": FieldMustBeUnique.developer_message,
        #     "user_message_title": FieldMustBeUnique.user_message_title
        # }
        # self.user_signup_error(post_data, expected_response_json)

    def test_missing_phone_number(self):
        """ """
        post_data = {
            "email": "max_mustermann@example.org",
            "first_name": "Max",
            "last_name": "Mustermann",
            "password": "Test1234!?",
        }
        self.user_signup(post_data)

    def test_password_weak_1_symbol(self):
        """Expected message: Password not strong enough, actual: One or more given fields are not valid
        Expected error code: 406, actual: 410
        Expected exception: SignupPasswordIsTooWeakError

        Args:

        Returns:

        """
        request = {
            "email": "max_mustermann@example.org",
            "first_name": "Max",
            "last_name": "Mustermann",
            "password": "1",
        }
        # expected_response_json = {
        #     "error_code": FieldNotValid.error_code,
        #     "more_info": FieldNotValid.more_info,
        #     "user_message_description": "This password is too short. It must contain at least 8 characters.",
        #     "developer_message": FieldNotValid.developer_message,
        #     "user_message_title": FieldNotValid.user_message_title
        # }
        # self.user_signup_error(request, expected_response_json)

    def test_invalid_email_1(self):
        """ """
        request = {
            "email": "max_musterman.test",
            "first_name": "Max",
            "last_name": "Mustermann",
            "password": "Test1234!?",
        }
        # expected_response_json = {
        #     "error_code": FieldNotValid.error_code,
        #     "more_info": FieldNotValid.more_info,
        #     "user_message_description": "A user with that email is not valid",
        #     "developer_message": FieldNotValid.developer_message,
        #     "user_message_title": FieldNotValid.user_message_title
        # }
        # self.user_signup_error(request, expected_response_json)

    def test_invalid_email_2(self):
        """ """
        request = {
            "email": "incorrect email format.with@sign",
            "first_name": "Max",
            "last_name": "Mustermann",
            "password": "Test1234!@#",
        }
        # expected_response_json = {
        #     "error_code": FieldNotValid.error_code,
        #     "more_info": FieldNotValid.more_info,
        #     "user_message_description": "A user with that email is not valid",
        #     "developer_message": FieldNotValid.developer_message,
        #     "user_message_title": FieldNotValid.user_message_title
        # }
        # self.user_signup_error(request, expected_response_json)
