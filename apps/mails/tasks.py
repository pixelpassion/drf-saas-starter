from datetime import datetime

from main.celery import app
from sendgrid.helpers.mail import *

from .models import Mail


def send_asynchronous_mail(self, mail_uuid, sendgrid_api=False):
    """ Queues an asynchronous mail, saves time queued"""
    try:
        mail = Mail.objects.get(id=mail_uuid)

        mail.time_queued = datetime.now()
        mail.save()
    except Mail.DoesNotExist:
        raise AttributeError("There is no mail with that UUID")
    
    send_asynchronous_mail_queud(self, mail_uuid, sendgrid_api)

    
@app.task(bind=True)
def send_asynchronous_mail_queued(self, mail_uuid, sendgrid_api=False):
    """ Sends an asynchronous mail by the given ID"""
    try:
        mail = Mail.objects.get(id=mail_uuid)
    except Mail.DoesNotExist:
        raise AttributeError("There is no mail with that UUID")

    mail.send(sendgrid_api=sendgrid_api)
