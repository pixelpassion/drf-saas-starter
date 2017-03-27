from rest_framework_jwt.test import APIJWTClient

from apps.users.models import User
from django.core import mail
from django.test import TestCase


import logging
logger = logging.getLogger(name=__name__)


class APITestCase(TestCase):
    """ """

    def setUp(self):
        """ """
        super(APITestCase, self).setUp()

        # Create an already existing up test user
        self.already_registered_user = User.objects.create(
            email='already_existing@example.com',
            password='test1234',
            first_name='Albus',
            last_name='Dumbledore'
        )

        self.base_api_url = "/api/"
        self.api_client = APIJWTClient

        # Clean the mail outbox, it would count to the tests if not
        mail.outbox = []
