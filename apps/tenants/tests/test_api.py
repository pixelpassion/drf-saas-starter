import json

from django.conf import settings
from django.contrib.sites.models import Site
from django.core import mail
from django.test import TestCase, override_settings

from apps.api.unit_tests import APITestCase
from apps.tenants.models import Tenant
from apps.users.models import User


class SingleTest(TestCase):
    """ Testing the Site creation
    
    """

    def test_django_site_setup(self):

        Site.objects.create(name="foo", domain="foo.com")


@override_settings(LANGUAGE_CODE='en')
class TenantSignupTests(TestCase):
    """ Test the sign_up process of the API endpoint """

    def setUp(self):
        """ The TENANT_DOMAIN is not used in tests because the sites migration is not loaded because of the bug (check settings.py)
            Until then example.com is used as a default domain in testing.
        """

        self.tenant_domain = Tenant.objects.get_tenant_domain()

        self.domain = "example.com"

        self.sign_up_url = "/api/sign_up/"

        self.already_registered_user_email = f'first@{self.tenant_domain}'
        self.already_registered_company_name = 'We are first'
        self.already_registered_company_domain = 'first'

        self.tenant_domain = Tenant.objects.get_tenant_domain()

        already_existing_site = Site.objects.get(domain=self.domain)
        already_existing_subdomain = f"{self.already_registered_company_domain}.{already_existing_site.domain}"

        Site.objects.get_or_create(name="First", domain=already_existing_subdomain)

        Tenant.objects.create(name=self.already_registered_company_name, site=already_existing_site)
        User.objects.create(email=self.already_registered_user_email, first_name="Was", last_name="First")

        # Clean the mail outbox, it would count to the tests if not
        mail.outbox = []

    def sign_up(self, post_data):
        """ Helper method for the correct sign_up """

        response = self.client.post(self.sign_up_url, json.dumps(post_data), content_type="application/json",  HTTP_HOST=self.domain)
        response_json = json.loads(response.content.decode('utf8'))

        self.assertEqual(response.status_code, 201, "Response code for adding user is incorrect! \n %s" % str(response_json))

        # User, Site and Tenant models should be around
        user = User.objects.get(email="awesome-ceo@example.com")

        correct_subdomain = "awesome.{}".format(self.tenant_domain)
        site = Site.objects.get(name=correct_subdomain, domain=correct_subdomain)

        tenant = Tenant.objects.get(name="Awesome customer", site=site)

        # User should be in the Tenants group
        self.assertTrue(tenant in user.tenants.all())

        # User should not be active
        self.assertFalse(user.is_active)

        # Tenant should not be active
        self.assertFalse(tenant.is_active)

        # An activation email should be sent
        # self.assertEqual(len(mail.outbox), 1)

    def sign_up_error(self, post_data, expected_error, expected_status_code=400):
        """ Helper method for an faulty sign_up """

        response = self.client.post(self.sign_up_url, json.dumps(post_data), content_type="application/json", HTTP_HOST=self.domain)
        self.assertContains(response, expected_error, status_code=expected_status_code)

        # There should be no created models
        self.assertEquals(User.objects.filter(email="awesome-ceo@example.com").count(), 0)
        self.assertEquals(Tenant.objects.filter(name="Awesome customer").count(), 0)
        self.assertEquals(Site.objects.filter(domain="awesome.{}".format(self.tenant_domain)).count(), 0)

        # No activation email should be sent
        # self.assertEqual(len(mail.outbox), 0)

    def test_correct_minimum_sign_up_data(self):
        """ """

        post_data = {
            "name": "Awesome customer",
            "domain": "awesome",
            "user": {
                "email": "awesome-ceo@example.com",
                "password": "a-w-e-s-o-m-e-1234"
            }
        }

        self.sign_up(post_data)

    def test_correct_optional_sign_up_data(self):
        """ """

        post_data = {
            "name": "Awesome customer",
            "domain": "awesome",
            "user": {
                "first_name": "Mr.",
                "last_name": "Awesome",
                "email": "awesome-ceo@example.com",
                "password": "a-w-e-s-o-m-e-1234"
            }
        }

        self.sign_up(post_data)

        # The user should have a first and last_name
        user = User.objects.get(email="awesome-ceo@example.com", first_name="Mr.", last_name="Awesome")

    def test_missing_email(self):
        """ """

        post_data = {
            "name": "Awesome customer",
            "domain": "awesome",
            "user": {
                "password": "awesome1234"
            }
        }

        self.sign_up_error(post_data, "This field is required")

    def test_already_existing_email(self):
        """ """

        post_data = {
            "name": "Awesome customer",
            "domain": "awesome",
            "user": {
                "email": self.already_registered_user_email,
                "password": "awesome1234"
            }
        }

        self.sign_up_error(post_data, "user with this email address already exists")

    def test_invalid_email(self):
        """ """

        post_data = {
            "name": "Awesome customer",
            "domain": "awesome",
            "user": {
                "email": "sadly@email",
                "password": "awesome1234"
            }
        }

        self.sign_up_error(post_data, "Enter a valid email address")

    def test_missing_password(self):
        """ """

        post_data = {
            "name": "Awesome customer",
            "domain": "awesome",
            "user": {
                "email": "awesome-ceo@example.com",
            }
        }

        self.sign_up_error(post_data, "This field is required")

    def test_missing_name(self):
        """ """

        post_data = {
            "domain": "awesome",
            "user": {
                "email": "awesome-ceo@example.com",
                "password": "awesome1234"
            }
        }

        self.sign_up_error(post_data, "This field is required")

    def test_already_existing_name(self):
        """ """

        post_data = {
            "name": self.already_registered_company_name,
            "domain": "awesome",
            "user": {
                "email": "awesome-ceo@example.com",
                "password": "awesome1234"
            }
        }

        self.sign_up_error(post_data, "tenant with this name already exists")

    def test_missing_domain(self):
        """ """

        post_data = {
            "name": "Awesome customer",
            "user": {
                "email": "awesome-ceo@example.com",
                "password": "awesome1234"
            }
        }

        self.sign_up_error(post_data, "This field is required")

    def test_already_existing_domain(self):
        """ """

        post_data = {
            "name": "Awesome customer",
            "domain": self.already_registered_company_domain,
            "user": {
                "email": "awesome-ceo@example.com",
                "password": "test1234"
            }
        }

        self.sign_up_error(post_data, "There is already an domain with that name")

    def test_password_to_short(self):
        """ """

        post_data = {
            "name": "Awesome customer",
            "domain": "awesome",
            "user": {
                "email": "awesome-ceo@example.com",
                "password": "z123"
            }
        }

        self.sign_up_error(post_data, "This password is too short")

    def test_password_too_close_to_email(self):
        """ """

        post_data = {
            "name": "Awesome customer",
            "domain": "awesome",
            "user": {
                "email": "awesome-ceo@example.com",
                "password": "awesome"
            }
        }

        self.sign_up_error(post_data, "The password is too similar to the email address")

    def test_password_with_only_numbers(self):
        """ """

        post_data = {
            "name": "Awesome customer",
            "domain": "awesome",
            "user": {
                "email": "awesome-ceo@example.com",
                "password": "12345678"
            }
        }

        self.sign_up_error(post_data, "This password is entirely numeric")

    def test_password_too_common(self):
        """ """

        post_data = {
            "name": "Awesome customer",
            "domain": "awesome",
            "user": {
                "email": "awesome-ceo@example.com",
                "password": "password1"
            }
        }

        self.sign_up_error(post_data, "This password is too common")


class SignupApiTests(APITestCase):
    """ Test the signup process of the API endpoint """

    def setUp(self):
        """ """
        super(SignupApiTests, self).setUp()
        self.signup_url = "%s/sign_up/"

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
        # post_data = {
        #     "email": self.already_registered_user_email,
        #     "first_name": self.already_registered_user.first_name,
        #     "last_name": self.already_registered_user.last_name,
        #     "password": self.already_registered_user_password,
        # }

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
        # user = self.user_signup(post_data)

        # # Token should be
        # self.assertIsNotNone(user.activation_token)
        #
        # # Token should have been created and have an decent length
        # if not settings.AUTO_ACCOUNT_ACTIVATION:
        #     self.assertTrue(len(user.activation_token) > 50)
        #
        # # Activation email is sent correctly
        # self.assertEqual(len(mail.outbox), 1)
        # self.assertEqual(mail.outbox[0].subject, u"Untitled project Account Activation")
        #
        # # The email should contain the generated token
        # activation_link = self.base_activation_url % user.activation_token
        # self.assertIn("%s%s" % (settings.BASE_URL, activation_link), mail.outbox[0].body)

    def test_user_activation(self):
        """ """
        email = 'max_mustermann@example.org'
        post_data = {
            "email": "%s" % email,
            "first_name": "Max",
            "last_name": "Mustermann",
            "password": "Test1234!?",
        }
        # user = self.user_signup(post_data)
        # self.activate_user(user)

    def test_missing_password(self):
        """
        """
        request = {
            "email": "max_mustermann@example.org",
            "first_name": "Max",
            "last_name": "Mustermann",
        }
        # response = self.client.post(self.signup_url, request)
        # response_json = json.loads(response.content.decode('utf8'))
        #
        # self.assertEqual(response.status_code, 400,
        #                  "Response code for adding user is incorrect! \n %s" %
        #                  str(response_json))
        # expected_response_json = {
        #     "error_code": EmailAndPasswordNeeded.error_code,
        #     "more_info": EmailAndPasswordNeeded.more_info,
        #     "user_message_description": EmailAndPasswordNeeded.user_message,
        #     "developer_message": EmailAndPasswordNeeded.developer_message,
        #     "user_message_title": EmailAndPasswordNeeded.user_message_title
        # }
        # self.assertEquals(response_json, expected_response_json)

    def test_missing_email(self):
        """ """
        request = {
            "first_name": "Max",
            "last_name": "Mustermann",
            "password": "Test1234!?",
        }
        # response = self.client.post(self.signup_url, request)
        # response_json = json.loads(response.content.decode('utf8'))
        #
        # self.assertEqual(response.status_code, 400,
        #                  "Response code for adding user is incorrect! \n %s" %
        #                  str(response_json))
        # expected_response_json = {
        #     "error_code": EmailAndPasswordNeeded.error_code,
        #     "more_info": EmailAndPasswordNeeded.more_info,
        #     "user_message_description": EmailAndPasswordNeeded.user_message,
        #     "developer_message": EmailAndPasswordNeeded.developer_message,
        #     "user_message_title": EmailAndPasswordNeeded.user_message_title
        # }
        # self.assertEquals(response_json, expected_response_json)

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
        # self.user_signup_error(post_data, expected_response_json)

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
        # self.user_signup(post_data)

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
