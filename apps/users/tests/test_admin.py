from django.test import TestCase

from..models import User
from ..admin import MyUserCreationForm


class TestMyUserCreationForm(TestCase):

    def setUp(self):
        self.existing_user = User.objects.create_user(email="existing_user@test.com", username="existing_user")

    def test_clean_username_success(self):
        # Instantiate the form with a new username
        form = MyUserCreationForm({
            'username': 'alamode',
            'password1': 'test1234',
            'password2': 'test1234',
        })
        # Run is_valid() to trigger the validation
        valid = form.is_valid()
        self.assertTrue(valid)

        # Run the actual clean_username method
        username = form.clean_username()
        self.assertEqual('alamode', username)

    def test_clean_username_false(self):
        # Instantiate the form with the same username as self.user
        form = MyUserCreationForm({
            'username': self.existing_user.username,
            'password1': 'test1234',
            'password2': 'test1234',
        })
        # Run is_valid() to trigger the validation, which is going to fail
        # because the username is already taken
        valid = form.is_valid()
        self.assertFalse(valid)

        # The form.errors dict should contain a single error called 'username'
        self.assertTrue(len(form.errors) == 1)
        self.assertTrue('username' in form.errors)
