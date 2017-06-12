from .models import Mail
from .tasks import send_asynchronous_mail


def create_and_send_mail(**kwargs):
    """Helper method to create and send a mail at once.

    create_and_send_mail(template_name="hello", context={'name': 'Jens'}, to_address="me@jensneuhaus.de")
    """
    mail = Mail.objects.create_mail(**kwargs)
    send_asynchronous_mail.delay(mail.id)
