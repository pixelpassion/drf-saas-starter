from django.db import models

from django.core.mail import EmailMessage, EmailMultiAlternatives

from django.template.loader import render_to_string, get_template
from django.template import TemplateDoesNotExist


class Mail(models.Model):
    MAX_CHARFIELD_LENGTH = 500
    
    from_address = models.EmailField()
    to_address = models.EmailField()

    sendgrid_id = models.IntegerField(default=0)
    sendgrid_delivery_status = models.IntegerField(default=0)

    template = models.CharField(max_length=MAX_CHARFIELD_LENGTH)
    subject = models.CharField(max_length=MAX_CHARFIELD_LENGTH)
    context = models.TextField()

    time_queued = models.DateTimeField()
    time_sent = models.DateTimeField()
    time_delivered = models.DateTimeField()

    # Create a Mail object with proper validation
    def create_mail(self, params):
        pass # to-do: implement this
    
    
    # Sends the mail using data from the Mail object
    def send(self):
        # Determine which templates exist
        try:
            txt_content = render_to_string(
                "{}.txt".format(self.template),
                self.context
            )
        except TemplateDoesNotExist:
            txt_content = None

        try:
            html_content = render_to_string(
                "{}.html".format(self.template), 
                self.context
            )
        except TemplateDoesNotExist:
            html_content = None

        # Send both text and html
        if txt_content and html_content:
            msg = EmailMultiAlternatives(
                self.subject, 
                txt_content,
                self.from_address, 
                [self.to_address]
            )
            msg.attach_alternative(html_content, "text/html")

        # Send text only
        elif txt_content:
            msg = EmailMessage(
                self.subject,
                txt_content,
                self.from_address,
                [self.to_address]
            )
 
        # Send html only
        elif html_content:
            msg = EmailMessage(
                self.subject,
                txt_content,
                self.from_address,
                [self.to_address]
            )
            msg.content_subtype = "html"

        # Throw error if no template was found
        else:
            pass # throw error here

        # Call send() to send the message
        msg.send()
        
