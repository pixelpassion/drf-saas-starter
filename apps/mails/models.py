from django.db import models

from django.core.mail import EmailMessage, EmailMultiAlternatives

from django.template.loader import render_to_string, get_template
from django.template import TemplateDoesNotExist
from main.mixins import UUIDMixin
from django.utils.translation import ugettext_lazy as _
from django.conf import *

class Mail(UUIDMixin):

    from_address = models.EmailField()
    to_address = models.EmailField()

    # delivery_service (Sendgrid etc. - should be a CharField with Options)

    delivery_mail_id = models.IntegerField(
        _("Unique mail sender ID"),
        help_text=_("The ID is saved after correct sending"),
        null=True,
        blank=True
    )

    # The following should maybe be a Charfield - depending on the anymail output
    delivery_status = models.IntegerField(
        _("Status of Mail sender"),
        help_text=_("The Mail sender status"),
        null=True,
        blank=True
    )

    template = models.CharField(
        _("Used Mail template"),
        help_text=_("The used text/HTML template - exists as a file"),
        max_length=50,
        null=False,
        blank=False)

    subject = models.CharField(max_length=500)
    context = models.TextField()

    time_queued = models.DateTimeField()
    time_sent = models.DateTimeField()
    time_delivered = models.DateTimeField()

    def __str__(self):
        return "%s to %s" % (self.template, self.to_address)

    @classmethod
    def create(cls, template, subject, context, to_address, from_address=None):
        """
            Create a Mail object with proper validation

            e.g.

            Mail.create("hello", "Hello world!",{'name': 'Jens'},"me@jensneuhaus.de"])
        """

        if from_address is None:
            from_address = settings.DEFAULT_FROM_EMAIL

        mail = cls(subject=subject, template=template, context=context, from_address=from_address, to_address=to_address)
        return mail

    def send(self):
        """
            Sends the mail using data from the Mail object

            Checks for existing template. Text is needed, HTML is optional.

            It can be called directly, but is usually called asynchronously.
         """

        try:
            txt_content = render_to_string(
                "mails/{}.txt".format(self.template),
                self.context
            )
        except TemplateDoesNotExist:
            raise ImportError("The txt-Template could not be found.")

        try:
            html_content = render_to_string(
                "mails/{}.html".format(self.template),
                self.context
            )
        except TemplateDoesNotExist:
            html_content = None

        if html_content:
            msg = EmailMultiAlternatives(
                self.subject,
                txt_content,
                self.from_address,
                [self.to_address]
            )
            msg.attach_alternative(html_content, "text/html")

        else:
            msg = EmailMessage(
                self.subject,
                txt_content,
                self.from_address,
                [self.to_address]
            )

        msg.send()

        print("Email with UUID {} was sent.".format(self.id))
