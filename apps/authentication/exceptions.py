from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from django.utils.translation import ugettext as _

from apps.api.exceptions import APIBaseException


class UserException(APIBaseException):
    """ """
    status_code = HTTP_400_BAD_REQUEST
    error_code = 400
    developer_message = _(u"There is an unspecific error for the entered data")
    user_message = _(u"There is an unspecific error - please try again later")


class AccessUnauthorized(APIBaseException):
    """ """
    status_code = HTTP_401_UNAUTHORIZED
    error_code = 401
    developer_message = _(u"The authentication for the user failed")
    user_message = _(u"You are not authenticated")


class OAuthTokenExpired(APIBaseException):
    """ """
    status_code = HTTP_401_UNAUTHORIZED
    error_code = 401
    developer_message = _(u"The access token has expired")
    user_message = _(u"You are not authenticated")


class UserNotActivated(APIBaseException):
    """ """
    status_code = HTTP_401_UNAUTHORIZED
    error_code = 401
    developer_message = _(u"The authentication for the user failed, because the user is deactivated")
    user_message = _('You did not activate your email yet - please click in the link in the email')


class UserBlocked(APIBaseException):
    """ """
    status_code = HTTP_401_UNAUTHORIZED
    error_code = 401
    developer_message = _(u"Maximimum login attempts exceeded")
    user_message = _(u"Your account is blocked. Contact the support team to reactivate it.")


class UserWrongCredentials(APIBaseException):
    """ """
    status_code = HTTP_401_UNAUTHORIZED
    error_code = 401
    developer_message = _(u"Credentials were wrong")
    user_message = _(u"Your email and/or password do not match")


class UserIsDeactivatedError(APIBaseException):
    """ """
    error_code = 405
    user_message = _(u'Your account is deactived')
    developer_message = _(u'The user is deactived')


class PasswordIsTooWeakError(APIBaseException):
    """ """
    error_code = 406
    user_message = _(u'Password not strong enough')
    developer_message = _(u'Password not accepted')


class EmailAndPasswordNeeded(APIBaseException):
    """ """
    error_code = 406
    user_message = _(u'You need to fill out email and password')
    developer_message = _(u'Password and email are missing')


class NewPasswordNeeded(APIBaseException):
    """ """
    error_code = 407
    user_message = _(u'You need to fill out password')
    developer_message = _(u'New password is missing')


class SamePasswords(APIBaseException):
    """ """
    error_code = 408
    user_message = _(u'Old password and new password are the same')
    developer_message = _(u'Old password and new password are the same')


class PasswordAlreadyUsed(APIBaseException):
    """ """
    error_code = 409
    user_message = _(u'Password can only be used once')
    developer_message = _(u'Password already used')
