
from main.celery import app
from sendgrid.helpers.mail import *

from .models import Mail


# import sendgrid
# from django.conf import settings
#
# @app.task(bind=True)
# def send_sendgrid_mail(self, context_dict):
#     """
#     From the anymail class, would be better to use the class
#     """
#
#     if not settings.SENDGRID_API_KEY:
#         raise NotImplementedError("No SENDGRID_API_KEY set")
#
#     sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)
#     from_email = Email("me@jensneuhaus.de")
#     to_email = Email("kontakt@jensneuhaus.de")
#     subject = "Sending with SendGrid is Fun: %s" % context_dict['number']
#     content = Content("text/plain", "and easy to do anywhere, even with Python")
#     mail = Mail(from_email, subject, to_email, content)
#     response = sg.client.mail.send.post(request_body=mail.get())
#     print(response.status_code)
#     print(response.body)
#     print(response.headers)


@app.task(bind=True)
def send_asynchronous_mail(self, mail_uuid):
    """ Sends an asynchronous mail by the given ID"""

    try:
        mail = Mail.objects.get(id=mail_uuid)
    except Mail.DoesNotExist:
        raise AttributeError("There is no mail with that UUID")

    mail.send()
