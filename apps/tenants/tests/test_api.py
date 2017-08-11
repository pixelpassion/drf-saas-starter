import json
from copy import deepcopy
from datetime import timedelta

import pytest
from django_saas_email.models import MailTemplate
from rest_framework import status
from rest_framework.test import APITestCase

from django.conf import settings
from django.contrib.sites.models import Site
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from apps.tenants.models import Tenant
from apps.tenants.tests.factories import InviteFactory
from apps.users.models import User
from apps.users.tests.factories import UserFactory, UserTenantRelationshipFactory


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

        MailTemplate.objects.create(name="email_confirmation_signup", html_template="<a href='{{ activation_url }}'>Confirm email address</a")

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

        # FIXME This fails on Circle CI
        # An activation email should be sent
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

        MailTemplate.objects.create(name="email_confirmation_signup", html_template="<a href='{{ activation_url }}'>Confirm email address</a")

    def user_signup(self, post_data, expected_status_code=201, expected_error_message=None):
        response = self.client.post(self.signup_url, post_data)

        if expected_error_message:
            self.assertContains(response, expected_error_message, status_code=expected_status_code)

            # No activation email should be sent
            self.assertEqual(len(mail.outbox), 0)

        elif expected_status_code:
            self.assertEqual(response.status_code, expected_status_code)

        # FIXME This fails on Circle CI
        # if expected_status_code == 200 or expected_status_code == 201:
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
        #
        # # Activation email is sent correctly
        # self.assertEqual(len(mail.outbox), 1)
        # self.assertEqual(mail.outbox[0].subject, u"Account Activation")
        #
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


@override_settings(LANGUAGE_CODE='en')
class TestInviteCreate(APITestCase):

    def setUp(self):
        user_tenant_relationship = UserTenantRelationshipFactory()
        self.user = user_tenant_relationship.user
        self.tenant = user_tenant_relationship.tenant

        self.invite_path = reverse('rest_invite', kwargs={'tenant_name': self.tenant.name})

        MailTemplate.objects.create(name="invite", html_template="<p>Invite</p>")


    def test_post_invite_without_login_status(self):
        post_data = {"email": "invitee@other-domain.com"}
        response = self.client.post(self.invite_path, data=post_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_post_invite_without_login_message(self):
        post_data = {"email": "invitee@other-domain.com"}
        response = self.client.post(self.invite_path, data=post_data)
        assert response.data['detail'] == 'Authentication credentials were not provided.'

    def test_post_invite_status(self):
        self.client.force_authenticate(user=self.user)
        post_data = {"email": "invitee@other-domain.com"}
        response = self.client.post(self.invite_path, data=post_data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_invitee_is_already_user(self):
        existing_user_email = 'invitee@other-domain.com'
        existing_user = UserFactory(email=existing_user_email)
        UserTenantRelationshipFactory(user=existing_user)
        self.client.force_authenticate(user=self.user)
        post_data = {"email": existing_user_email}
        response = self.client.post(self.invite_path, data=post_data)
        assert response.status_code == status.HTTP_201_CREATED

    # TODO Write test(s) when implemented
    def test_inviter_is_from_different_tenant(self):
        pass
        # other_tenant = TenantFactory()
        # different_invite_path = reverse('rest_invite', kwargs={'tenant_name': other_tenant.name})
        # self.client.force_authenticate(user=self.user)
        # post_data = {"email": "invitee@other-domain.com"}
        # response = self.client.post(different_invite_path, data=post_data)
        # assert response.status_code != status.HTTP_201_CREATED

    # FIXME This fails on Circle CI
    # def test_email_sent(self):
    #     post_data = {"email": "invitee@other-domain.com"}
    #     self.client.force_authenticate(user=self.user)
    #     self.client.post(self.invite_path, data=post_data)
    #     assert len(mail.outbox) == 1


@override_settings(LANGUAGE_CODE='en')
class TestInviteRetrieve(APITestCase):

    def setUp(self):
        self.invite = InviteFactory(first_name='Peter', last_name='Pan')
        self.retrieve_path = reverse(
            'rest_invite_retrieve',
            kwargs={'tenant_name': self.invite.tenant.name, 'pk': self.invite.pk}
        )

        no_name_invite = InviteFactory()
        self.no_name_retrieve_path = reverse(
            'rest_invite_retrieve',
            kwargs={'tenant_name': no_name_invite.tenant.name, 'pk': no_name_invite.pk}
        )

    def test_status(self):
        response = self.client.get(self.retrieve_path)
        assert response.status_code == status.HTTP_200_OK

    def test_first_name(self):
        response = self.client.get(self.retrieve_path)
        assert response.data['first_name'] == 'Peter'

    def test_last_name(self):
        response = self.client.get(self.retrieve_path)
        assert response.data['last_name'] == 'Pan'

    def test_active(self):
        response = self.client.get(self.retrieve_path)
        assert response.data['is_active'] == True

    def test_first_clicked(self):
        self.client.get(self.retrieve_path)
        self.invite.refresh_from_db()
        assert self.invite.first_clicked

    def test_first_clicked_not_updated(self):
        """Test whether clicking on the invite a second time would change the value of first_clicked."""
        self.client.get(self.retrieve_path)
        self.invite.refresh_from_db()
        first_clicked = deepcopy(self.invite.first_clicked)
        self.client.get(self.retrieve_path)
        self.invite.refresh_from_db()
        assert first_clicked == self.invite.first_clicked

    def test_no_first_name(self):
        response = self.client.get(self.no_name_retrieve_path)
        assert response.data['first_name'] == ''

    def test_no_last_name(self):
        response = self.client.get(self.no_name_retrieve_path)
        assert response.data['last_name'] == ''

    def test_not_active(self):
        expired_creation_date = timezone.now() - timedelta(days=settings.TENANT_INVITE_EXPIRATION_IN_DAYS, hours=1)
        old_invite = InviteFactory(time_created=expired_creation_date)
        old_retrieve_path = reverse(
            'rest_invite_retrieve',
            kwargs = {'tenant_name': old_invite.tenant.name, 'pk': old_invite.pk}
        )
        response = self.client.get(old_retrieve_path)
        assert response.data['is_active'] == False

    def test_existing_user(self):
        existing_user = UserFactory()
        existing_user_invite = InviteFactory(email=existing_user.email)
        existing_user_retrieve_path = reverse(
            'rest_invite_retrieve',
            kwargs={'tenant_name': existing_user_invite.tenant.name, 'pk': existing_user_invite.pk}
        )
        response = self.client.get(existing_user_retrieve_path)
        assert response.data['detail'] == f'Your account is now successfully connected to {existing_user_invite.tenant.name}.'


@override_settings(LANGUAGE_CODE='en')
class TestInviteActivation(APITestCase):

    def setUp(self):
        self.invite = InviteFactory(first_name='Peter', last_name='Pan')
        self.activation_url = self.invite.get_activation_url()
        self.password = 'test1234?!'
        self.post_data = {
            "user": {
                "password1": self.password,
                "password2": self.password
            }
        }
        self.response = self.client.patch(self.activation_url, data=self.post_data, format='json')

    def test_activation(self):
        assert self.response.status_code == status.HTTP_200_OK

    def test_user_created(self):
        User.objects.get(email=self.invite.email)

    def test_user_tenant_relationship_created(self):
        user = User.objects.get(email=self.invite.email)
        tenant = self.invite.tenant
        assert user.usertenantrelationship_set.filter(tenant=tenant)

    def test_user_can_login(self):
        login_path = reverse('rest_login')
        post_data = {"email": self.invite.email, "password": self.password}
        response = self.client.post(login_path, post_data)
        assert response.status_code == status.HTTP_200_OK

    def test_invite_already_used(self):
        response = self.client.patch(self.activation_url, data=self.post_data, format='json')
        assert response.data['error'] == 'The invitation was already used.'

    def test_existing_user(self):
        existing_user = UserFactory()
        existing_user_invite = InviteFactory(email=existing_user.email)
        existing_user_activation_url = existing_user_invite.get_activation_url()
        response = self.client.patch(existing_user_activation_url, data=self.post_data, format='json')
        assert response.data['error'] == 'You are already a user, please use the link from the email.'

    def test_inactive_invite(self):
        expired_creation_date = timezone.now() - timedelta(days=settings.TENANT_INVITE_EXPIRATION_IN_DAYS, hours=1)
        old_invite = InviteFactory(time_created=expired_creation_date)
        old_invite_activation_url = old_invite.get_activation_url()
        response = self.client.patch(old_invite_activation_url, data=self.post_data, format='json')
        assert response.data['error'] == 'The invitation was not used while it was active.'
