from django.db.utils import IntegrityError
from django.test import TestCase

from ..models import User


class TestUser(TestCase):

    def setUp(self):
        self.existing_user = User.objects.create_user(
            email="existing_user@test.com",
            first_name="Existing",
            last_name="User",
            username="existing_user")

    def test__str__(self):
        self.assertEqual(
            self.existing_user.__str__(),
            'Existing User'
        )

    def test__short_name(self):
        self.assertEqual(
            self.existing_user.get_short_name(),
            'existing_user'
        )

    def test__full_name(self):
        self.assertEqual(
            self.existing_user.get_full_name(),
            'Existing User'
        )

    def test_get_absolute_url(self):
        self.assertEqual(
            self.existing_user.get_absolute_url(),
            f"admin/users/user/{self.existing_user.id}/change/"
        )

    def test_create_user_method(self):
        """We are checking, if we can create a user with just an email."""
        new_user = User.objects.create_user(email="new_user@test.com")
        self.assertEqual(User.objects.get(email="new_user@test.com"), new_user)
        self.assertEqual(new_user.is_staff, False)
        self.assertEqual(new_user.is_superuser, False)

    def test_create_user_with_ungiven_username(self):
        """We are checking, if we can create a user with just an email."""
        new_user = User.objects.create_user(email="username@test.com")
        self.assertEqual(new_user.username, "username")

    def test_create_user_with_existing_email(self):
        """We are checking, if we can create a user with just an email."""
        with self.assertRaises(IntegrityError):
            User.objects.create_user(email="existing_user@test.com")

    def test_create_user_with_existing_username(self):
        """We are checking, if we can create a user with just an email."""
        with self.assertRaises(IntegrityError):
            User.objects.create_user(email="existing_user2@test.com", username="existing_user")

    def test_create_user_with_existing_username_method(self):
        """We are checking, if we can create a user with just an email."""
        new_user = User.objects.create_user(email="new_user@test.com", password="test")
        self.assertEqual(User.objects.get(email="new_user@test.com"), new_user)
        self.assertEqual(new_user.has_usable_password(), True)

    def test_create_superuser_method(self):
        """We are checking, if we can create a user with just an email."""
        new_user = User.objects.create_superuser(email="new_user@test.com", password="test")
        self.assertEqual(User.objects.get(email="new_user@test.com"), new_user)
        self.assertEqual(new_user.has_usable_password(), True)
        self.assertEqual(new_user.is_staff, True)
        self.assertEqual(new_user.is_superuser, True)

    def test_find_next_available_username(self):
        """A unused and ungiven username should be given."""
        self.assertEqual(User.objects.find_next_available_username("not_used_yet"), "not_used_yet")

        i = 2

        # The next available existing_user should have a username with 2
        while i < 12:
            self.assertEqual(User.objects.find_next_available_username("existing_user"), "existing_user{}".format(i))
            User.objects.create_user(email="existing_user@test{}.com".format(i), password="test")
            i += 1
