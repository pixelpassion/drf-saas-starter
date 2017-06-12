import json

import pytest

from django.contrib.sites.models import Site
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from apps.tenants.models import Tenant
from apps.users.models import User


@override_settings(LANGUAGE_CODE='en')
class TenantSignupTests(TestCase):
    """Test the signup process for a new tenant."""

    def setUp(self):
        # The TENANT_ROOT_DOMAIN is not used in tests because the sites migration is not loaded
        # because of a bug (check settings.py)
        # Until then example.com is used as a default domain in testing.
        self.tenant_root_domain = Tenant.objects.get_tenant_root_domain()

        self.sign_up_url = reverse("tenant_rest_register")

        self.already_registered_user_email = f'first@{self.tenant_root_domain}'
        self.already_registered_company_name = 'We are first'
        self.already_registered_company_domain = 'first'

        already_existing_site = Site.objects.get(domain=self.tenant_root_domain)
        already_existing_subdomain = f"{self.already_registered_company_domain}.{already_existing_site.domain}"

        Site.objects.get_or_create(name="First", domain=already_existing_subdomain)

        Tenant.objects.create(name=self.already_registered_company_name, site=already_existing_site)
        User.objects.create(email=self.already_registered_user_email, first_name="Was", last_name="First")

        # Clean the mail outbox, it would count to the tests if not
        mail.outbox = []

    def sign_up(self, post_data):
        """Helper method for the correct signup."""

        response = self.client.post(
            self.sign_up_url,
            json.dumps(post_data),
            content_type="application/json",
            HTTP_HOST=self.tenant_root_domain
        )
        response_json = json.loads(response.content.decode('utf8'))

        self.assertEqual(
            response.status_code,
            201,
            "Response code for adding user is incorrect! \n %s" % str(response_json))

        # Give an info about the sent verification email
        self.assertContains(response, "Verification e-mail sent", status_code=201)

        # User, Site and Tenant models should be around
        user = User.objects.get(email="awesome-ceo@example.com")

        correct_subdomain = "awesome.{}".format(self.tenant_root_domain)
        site = Site.objects.get(name=correct_subdomain, domain=correct_subdomain)

        tenant = Tenant.objects.get(name="Awesome customer", site=site)

        # User should be in the Tenants group
        self.assertTrue(tenant in user.tenants.all())

        # User should not be active
        self.assertTrue(user.is_active)

        # Tenant should not be active
        self.assertFalse(tenant.is_active)

        # An activation email should be sent (uncommented, fails on CircleCI)
        # self.assertEqual(len(mail.outbox), 1)

    def sign_up_error(self, post_data, expected_error, expected_status_code=400):
        """Helper method for an faulty signup."""

        response = self.client.post(
            self.sign_up_url,
            json.dumps(post_data),
            content_type="application/json",
            HTTP_HOST=self.tenant_root_domain
        )

        self.assertContains(response, expected_error, status_code=expected_status_code)

        # There should be no created models
        self.assertEqual(User.objects.filter(email="awesome-ceo@example.com").count(), 0)
        self.assertEqual(Tenant.objects.filter(name="Awesome customer").count(), 0)
        self.assertEqual(Site.objects.filter(domain="awesome.{}".format(self.tenant_root_domain)).count(), 0)

        # No activation email should be sent
        self.assertEqual(len(mail.outbox), 0)

    def test_correct_minimum_sign_up_data(self):
        post_data = {
            "name": "Awesome customer",
            "subdomain": "awesome",
            "user": {
                "email": "awesome-ceo@example.com",
                "first_name": "Peter",
                "last_name": "Lustig",
                "password1": "a-w-e-s-o-m-e-1234",
                "password2": "a-w-e-s-o-m-e-1234"
            }
        }
        self.sign_up(post_data)

    def test_missing_email(self):
        post_data = {
            "name": "Awesome customer",
            "subdomain": "awesome",
            "user": {
                "first_name": "Max",
                "last_name": "Mustermann",
                "password1": "awesome1234",
                "password2": "awesome1234"
            }
        }
        self.sign_up_error(post_data, "This field is required")

    def test_already_existing_email(self):
        post_data = {
            "name": "Awesome customer",
            "subdomain": "awesome",
            "user": {
                "email": self.already_registered_user_email,
                "first_name": "Max",
                "last_name": "Mustermann",
                "password1": "awesome1234",
                "password2": "awesome1234"
            }
        }
        self.sign_up_error(post_data, "A user is already registered with this e-mail address")

    def test_empty_email(self):
        post_data = {
            "name": "Awesome customer",
            "subdomain": "awesome",
            "user": {
                "email": "",
                "first_name": "Max",
                "last_name": "Mustermann",
                "password1": "awesome1234",
                "password2": "awesome1234"
            }
        }
        self.sign_up_error(post_data, "This field may not be blank")

    def test_invalid_email(self):
        post_data = {
            "name": "Awesome customer",
            "subdomain": "awesome",
            "user": {
                "email": "sadly@email",
                "first_name": "Max",
                "last_name": "Mustermann",
                "password1": "awesome1234",
                "password2": "awesome1234"
            }
        }
        self.sign_up_error(post_data, "Enter a valid email address")

    def test_missing_first_name(self):
        post_data = {
            "name": "Awesome customer",
            "subdomain": "awesome",
            "user": {
                "email": "sadly@example.com",
                "last_name": "Mustermann",
                "password1": "awesome1234",
                "password2": "awesome1234"
            }
        }
        self.sign_up_error(post_data, "This field is required")

    def test_empty_first_name(self):
        post_data = {
            "name": "Awesome customer",
            "subdomain": "awesome",
            "user": {
                "email": "sadly@email",
                "first_name": "",
                "last_name": "Mustermann",
                "password1": "awesome1234",
                "password2": "awesome1234"
            }
        }
        self.sign_up_error(post_data, "This field may not be blank")

    def test_empty_last_name(self):
        post_data = {
            "name": "Awesome customer",
            "subdomain": "awesome",
            "user": {
                "email": "sadly@email",
                "first_name": "Max",
                "last_name": "",
                "password1": "awesome1234",
                "password2": "awesome1234"
            }
        }
        self.sign_up_error(post_data, "This field may not be blank")

    def test_missing_last_name(self):
        post_data = {
            "name": "Awesome customer",
            "subdomain": "awesome",
            "user": {
                "email": "sadly@email",
                "first_name": "Max",
                "password1": "awesome1234",
                "password2": "awesome1234"
            }
        }
        self.sign_up_error(post_data, "This field is required")

    def test_missing_password(self):
        post_data = {
            "name": "Awesome customer",
            "subdomain": "awesome",
            "user": {
                "email": "awesome-ceo@example.com",
                "first_name": "Max",
                "last_name": "Mustermann",
            }
        }
        self.sign_up_error(post_data, "This field is required")

    def test_password_mismatch(self):
        post_data = {
            "name": "Awesome customer",
            "subdomain": "awesome",
            "user": {
                "email": "awesome-ceo@example.com",
                "first_name": "Max",
                "last_name": "Mustermann",
                "password1": "awesome1234",
                "password2": "awesome1235"
            }
        }
        self.sign_up_error(post_data, "The two password fields didn\'t match")

    def test_missing_name(self):
        post_data = {
            "subdomain": "awesome",
            "user": {
                "email": "awesome-ceo@example.com",
                "first_name": "Max",
                "last_name": "Mustermann",
                "password1": "awesome1234",
                "password2": "awesome1234"
            }
        }
        self.sign_up_error(post_data, "This field is required")

    def test_already_existing_name(self):
        post_data = {
            "name": self.already_registered_company_name,
            "subdomain": "awesome",
            "user": {
                "email": "awesome-ceo@example.com",
                "first_name": "Max",
                "last_name": "Mustermann",
                "password1": "awesome1234",
                "password2": "awesome1234"
            }
        }
        self.sign_up_error(post_data, "tenant with this name already exists")

    def test_missing_domain(self):
        post_data = {
            "name": "Awesome customer",
            "user": {
                "email": "awesome-ceo@example.com",
                "first_name": "Max",
                "last_name": "Mustermann",
                "password1": "awesome1234",
                "password2": "awesome1234"
            }
        }
        self.sign_up_error(post_data, "This field is required")

    def test_already_existing_domain(self):
        post_data = {
            "name": "Awesome customer",
            "subdomain": self.already_registered_company_domain,
            "user": {
                "email": "awesome-ceo@example.com",
                "first_name": "Max",
                "last_name": "Mustermann",
                "password1": "awesome1234",
                "password2": "awesome1234"
            }
        }
        self.sign_up_error(post_data, "There is already an domain with that name")

    def test_password_to_short(self):
        post_data = {
            "name": "Awesome customer",
            "subdomain": "awesome",
            "user": {
                "email": "awesome-ceo@example.com",
                "first_name": "Max",
                "last_name": "Mustermann",
                "password1": "z123",
                "password2": "z123"
            }
        }
        self.sign_up_error(post_data, "This password is too short")

    @pytest.mark.skip(
        reason="This is not running through for now - check https://github.com/jensneuhaus/einhorn-starter/issues/65")
    def test_password_too_close_to_email(self):
        post_data = {
            "name": "Awesome customer",
            "subdomain": "awesome",
            "user": {
                "email": "awesome-ceo@example.com",
                "first_name": "Max",
                "last_name": "Mustermann",
                "password1": "awesome-ceo",
                "password2": "awesome-ceo"
            }
        }
        self.sign_up_error(post_data, "The password is too similar to the email address")

    def test_password_with_only_numbers(self):
        post_data = {
            "name": "Awesome customer",
            "subdomain": "awesome",
            "user": {
                "email": "awesome-ceo@example.com",
                "first_name": "Max",
                "last_name": "Mustermann",
                "password1": "12345678",
                "password2": "12345678"
            }
        }
        self.sign_up_error(post_data, "This password is entirely numeric")

    def test_password_too_common(self):
        post_data = {
            "name": "Awesome customer",
            "subdomain": "awesome",
            "user": {
                "email": "awesome-ceo@example.com",
                "password1": "password1",
                "password2": "password1"
            }
        }
        self.sign_up_error(post_data, "This password is too common")


@override_settings(LANGUAGE_CODE='en')
class UserSignupTests(TestCase):
    """Test the signup process of users."""

    def setUp(self):
        # Create valid tenant
        tenant_admin = User.objects.create_user(email="admin@example.com", first_name="Achim", last_name="Admin")
        self.tenant = Tenant.objects.create_tenant(tenant_admin, "tenant", "tenant")
        self.tenant.is_active = True
        self.tenant.save()

        self.signup_url = reverse('user_rest_register', kwargs={'tenant_name': self.tenant.name})

    def user_signup(self, post_data, expected_status_code=201, expected_error_message=None):
        response = self.client.post(self.signup_url, post_data)

        if expected_error_message:
            self.assertContains(response, expected_error_message, status_code=expected_status_code)

            # No activation email should be sent
            self.assertEqual(len(mail.outbox), 0)

        elif expected_status_code:
            self.assertEqual(response.status_code, expected_status_code)

        # FIXME Fails on CircleCI
        # if expected_status_code == 200 or expected_status_code == 201:
        #
        #     self.assertEqual(len(mail.outbox), 1)

    def test_correct_signup_data(self):
        post_data = {
            "email": "max_mustermann@example.org",
            "first_name": "Max",
            "last_name": "Mustermann",
            "password1": "Test1234!?",
            "password2": "Test1234!?"
        }
        self.user_signup(post_data)

    def test_deactivated_tenant(self):
        """The user should not be able to register, when the tenant is deactivated."""

        self.tenant.is_active = False
        self.tenant.save()

        post_data = {
            "email": "max_mustermann@example.org",
            "first_name": "Max",
            "last_name": "Mustermann",
            "password1": "Test1234!?",
            "password2": "Test1234!?"
        }

        self.user_signup(
            post_data,
            expected_status_code=400,
            expected_error_message="Tenant is deactivated, no registration is possible"
        )

    def test_already_existing_email(self):

        User.objects.create_user(email='alreadyexisting@example.com')

        post_data = {
            "email": 'alreadyexisting@example.com',
            "first_name": "Max",
            "last_name": "Mustermann",
            "password1": "Test1234!?",
            "password2": "Test1234!?"
        }

        self.user_signup(
            post_data,
            expected_status_code=400,
            expected_error_message="A user is already registered with this e-mail address"
        )

    def test_sending_of_activation_email(self):
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
        # self.assertEqual(mail.outbox[0].subject, u"Account Activation")
        #
        # # The email should contain the generated token
        # activation_link = self.base_activation_url % user.activation_token
        # self.assertIn("%s%s" % (settings.BASE_URL, activation_link), mail.outbox[0].body)

    def test_missing_password1(self):
        post_data = {
            "email": 'alreadyexisting@example.com',
            "first_name": "Max",
            "last_name": "Mustermann",
            "password2": "Test1234!?"
        }
        self.user_signup(post_data, expected_status_code=400, expected_error_message="This field is required")

    def test_missing_password2(self):
        post_data = {
            "email": 'alreadyexisting@example.com',
            "first_name": "Max",
            "last_name": "Mustermann",
            "password1": "Test1234!?",
        }
        self.user_signup(post_data, expected_status_code=400, expected_error_message="This field is required")

    def test_missing_password_mismatch(self):
        post_data = {
            "email": 'alreadyexisting@example.com',
            "first_name": "Max",
            "last_name": "Mustermann",
            "password1": "Test1234!?",
            "password2": "Test5678!?"
        }
        self.user_signup(
            post_data,
            expected_status_code=400,
            expected_error_message="The two password fields didn\'t match."
        )

    def test_missing_email(self):
        post_data = {
            "first_name": "Max",
            "last_name": "Mustermann",
            "password1": "Test1234!?",
            "password2": "Test1234!?"
        }
        self.user_signup(post_data, expected_status_code=400, expected_error_message="This field is required")

    def test_missing_first_name(self):
        post_data = {
            "email": 'alreadyexisting@example.com',
            "last_name": "Mustermann",
            "password1": "Test1234!?",
            "password2": "Test1234!?"
        }
        self.user_signup(post_data, expected_status_code=400, expected_error_message="This field is required")

    def test_missing_last_name(self):
        post_data = {
            "email": 'alreadyexisting@example.com',
            "first_name": "Max",
            "password1": "Test1234!?",
            "password2": "Test1234!?"
        }
        self.user_signup(post_data, expected_status_code=400, expected_error_message="This field is required")

    def test_password_weak_1_symbol(self):
        post_data = {
            "email": 'alreadyexisting@example.com',
            "first_name": "Max",
            "last_name": "Mustermann",
            "password1": "test12",
            "password2": "test12"
        }
        self.user_signup(
            post_data,
            expected_status_code=400,
            expected_error_message="This password is too short. It must contain at least 8 characters"
        )

    def test_invalid_email(self):
        post_data = {
            "email": 'alreadyexisting@example',
            "first_name": "Max",
            "last_name": "Mustermann",
            "password1": "Test1234!?",
            "password2": "Test1234!?"
        }
        self.user_signup(post_data, expected_status_code=400, expected_error_message="Enter a valid email address")
