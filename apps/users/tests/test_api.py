from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse

from ..models import User


class TestSuperuserLogin(APITestCase):

    def setUp(self):
        self.email = "new_user@test.com"
        self.password = "test1234"
        self.new_superuser = User.objects.create_superuser(email=self.email, password=self.password)
        self.login_path = reverse('rest_login')

    def test_create_superuser_login(self):
        """Check whether a created superuser is automatically verified and can use the login."""
        post_data = {"email": self.email, "password": self.password}
        response = self.client.post(self.login_path, data=post_data, format='json')
        assert response.status_code == status.HTTP_200_OK
