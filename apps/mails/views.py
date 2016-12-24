# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import sendgrid
from sendgrid.helpers.mail import *
from django.conf import settings


def test_mail():

    if not settings.SENDGRID_API_KEY:
        raise NotImplementedError("No SENDGRID_API_KEY set")

    sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)
    from_email = Email("me@jensneuhaus.de")
    to_email = Email("kontakt@jensneuhaus.de")
    subject = "Sending with SendGrid is Fun"
    content = Content("text/plain", "and easy to do anywhere, even with Python")
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)

