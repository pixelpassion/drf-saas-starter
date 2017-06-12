from allauth.account.models import EmailAddress
from allauth.account.utils import send_email_confirmation

from django.contrib.auth import user_logged_out


def logout_user(request):
    # authtoken.models.Token.objects.filter(user=request.user).delete()

    # Introduce a session_ID Flag in every session. Logout..

    user_logged_out.send(sender=request.user.__class__, request=request, user=request.user)


def send_email_verification(request, user, email_verification):

    has_verified_email = EmailAddress.objects.filter(user=user, verified=True).exists()

    if not has_verified_email:
        send_email_confirmation(request, user, signup=True)
