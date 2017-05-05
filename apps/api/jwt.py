import uuid
from calendar import timegm
from datetime import datetime

from rest_framework_jwt.compat import get_username, get_username_field
from rest_framework_jwt.settings import api_settings

from django.conf import settings


def payload_handler(user):
    """Function to generate the token payload

    {
      "iss": "einhorn-starter",
      "user_id": "4d92a809-4f68-4c19-b115-eaa1a0e5a170",
      "sub": "jens",
      "email": "kontakt@jensneuhaus.de",
      "groups": [
        "HR",
        "Test"
      ],
      "exp": 1487970010,
      "is_superuser": true
    }


    Who this person is (sub, short for subject)
    What this person can access with this token (scope)
    When the token expires (exp)
    Who issued the token (iss, short for issuer)



    """

    username_field = get_username_field()
    username = get_username(user)

    payload = {
        'sub': username,
        'is_superuser': user.is_superuser,
        'groups': list(user.groups.all().values_list('name', flat=True)),
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA,
        'iss': api_settings.JWT_ISSUER
    }
    if isinstance(user.pk, uuid.UUID):
        payload['user_id'] = str(user.pk)

    payload[username_field] = username

    # Include original issued at time for a brand new token,
    # to allow token refresh
    if api_settings.JWT_ALLOW_REFRESH:
        payload['orig_iat'] = timegm(
            datetime.utcnow().utctimetuple()
        )

    if api_settings.JWT_AUDIENCE is not None:
        payload['aud'] = api_settings.JWT_AUDIENCE

    if api_settings.JWT_ISSUER is not None:
        payload['iss'] = api_settings.JWT_ISSUER

    return payload


def response_payload_handler(token, user=None, request=None):
    """
    Returns the response data for both the login and refresh views.
    Override to return a custom response such as including the
    serialized representation of the User.
    Example:
    def jwt_response_payload_handler(token, user=None, request=None):
        return {
            'token': token,
            'user': UserSerializer(user, context={'request': request}).data
        }
    """
    return {
        'token': token,
    }


def get_username_from_payload_handler(payload):
    """
    Override this function if username is formatted differently in payload
    """
    return payload.get('email')
