from django.test import TestCase, override_settings

from ..admin import MyUserCreationForm

from..models import User


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


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class AdminSecurityTestCase(TestCase):
    """ Test the security of the admin"""

    def setUp(self):

        username = "superuser"
        email = "superuser@test.com"
        password = "test1234"

        self.superuser = User.objects.create_superuser(email=email, username=username, password=password)
        self.superuser.is_active = True
        self.superuser.save()

        self.login_url = "/admin/login/"

        self.login_data = {
            "username": username,
            "password": password
        }

        self.login_data_with_wrong_password = {
            "username": username,
            "password": "test1235"
        }

        self.completely_wrong_login_data= {
            "username": "wrongusername",
            "password": "test1235"
        }

    # def test_working_login(self):
    #
    #     response = self.client.post(self.login_url, self.login_data)
    #     self.assertEqual(response.status_code, 200)
    #     print(response.context)
    #     self.assertTrue(response.context['user'].is_authenticated)
    #
    # def test_brute_force_check(self):
    #
    #     response = self.client.post(self.login_url, self.login_data_with_wrong_password)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertFalse(response.context['user'].is_authenticated)
