import json
from django.test import TestCase, override_settings

from django.conf import settings

from apps.users.models import User
from apps.tenants.models import Tenant, Domain
from django.contrib.sites.models import Site

from django.core import mail

import logging
logger = logging.getLogger(name=__name__)


@override_settings(TENANT_DOMAIN="example.com", LANGUAGE_CODE='en')
class TenantSignupTests(TestCase):
    """ Test the sign_up process of the API endpoint """

    def setUp(self):
        """ """

        self.sign_up_url = "/api/sign_up/"

        self.already_registered_user_email = 'first@example.com'
        self.already_registered_company_name = 'We are first'
        self.already_registered_company_domain = 'first'

        already_existing_subdomain = "{}.{}".format(self.already_registered_company_domain, settings.TENANT_DOMAIN)
        already_existing_site = Site.objects.create(name=already_existing_subdomain, domain=already_existing_subdomain)

        Tenant.objects.create(name=self.already_registered_company_name, site=already_existing_site)
        User.objects.create(email=self.already_registered_user_email, first_name="Was", last_name="First")

        # Clean the mail outbox, it would count to the tests if not
        mail.outbox = []

    def sign_up(self, post_data):
        """ Helper method for the correct sign_up """

        response = self.client.post(self.sign_up_url, json.dumps(post_data), content_type="application/json",  HTTP_HOST="example.com")
        response_json = json.loads(response.content.decode('utf8'))

        self.assertEqual(response.status_code, 201, "Response code for adding user is incorrect! \n %s" % str(response_json))

        # User, Site and Tenant models should be around
        user = User.objects.get(email="awesome-ceo@example.com")

        correct_subdomain = "awesome.{}".format(settings.TENANT_DOMAIN)
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

        response = self.client.post(self.sign_up_url, json.dumps(post_data), content_type="application/json", HTTP_HOST="example.com")

        self.assertContains(response, expected_error, status_code=expected_status_code)

        # There should be no created models
        self.assertEquals(User.objects.filter(email="awesome-ceo@example.com").count(), 0)
        self.assertEquals(Tenant.objects.filter(name="Awesome customer").count(), 0)
        self.assertEquals(Site.objects.filter(domain="awesome.{}".format(settings.TENANT_DOMAIN)).count(), 0)

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
                "password": "awesome1234"
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
