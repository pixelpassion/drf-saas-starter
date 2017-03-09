from django.contrib.auth import user_logged_in, user_logged_out


def logout_user(request):
    #authtoken.models.Token.objects.filter(user=request.user).delete()

    # Introduce a session_ID Flag in every session. Logout..

    user_logged_out.send(sender=request.user.__class__, request=request, user=request.user)