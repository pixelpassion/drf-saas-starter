from main.celery import app
from sendgrid.helpers.mail import *

from django.utils import timezone

from .models import Mail


@app.task(bind=True)
def send_asynchronous_mail(self, mail_uuid, sendgrid_api=False):
    """ Sends an asynchronous mail by the given ID"""
    try:
        mail = Mail.objects.get(id=mail_uuid)
    except Mail.DoesNotExist:
        raise AttributeError("There is no mail with that UUID")

    mail.send(sendgrid_api=sendgrid_api)
