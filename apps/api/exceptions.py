from rest_framework.status import HTTP_422_UNPROCESSABLE_ENTITY, HTTP_500_INTERNAL_SERVER_ERROR
from django.utils.translation import ugettext as _


class APIBaseException(Exception):
    """ """
    status_code = HTTP_500_INTERNAL_SERVER_ERROR
    error_code = 100
    user_message = _(u"An unknown error happened - please try again later")
    developer_message = _(u"An unexpected error happened - please ask your local backend developer for assistance")
    more_info = None

    def add_user_message(self, message):
        """Ad an specific user message to an error"""
        self.user_message = message

    def add_developer_message(self, message):
        """Add an specific developer message to an error"""
        self.developer_message = message

    def add_status_code(self, status_code):
        """Add an specific status_code to an error"""
        self.status_code = status_code


class APIUseException(APIBaseException):
    """ """
    status_code = HTTP_422_UNPROCESSABLE_ENTITY
    error_code = 300
    developer_message = _(u"There is an unspecified error with this API call - please check the documentation")


