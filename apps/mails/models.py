from django.db import models

from django.core.mail import EmailMessage, EmailMultiAlternatives

from django.template.loader import render_to_string, get_template
from django.template import TemplateDoesNotExist
from main.mixins import UUIDMixin
from django.utils.translation import ugettext_lazy as _
from django.conf import *
import sendgrid

if not settings.SENDGRID_API_KEY:
    raise NotImplementedError("No SENDGRID_API_KEY set")

sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)

MAIL_TEMPLATES = {
    "action": {
        "template": "transactional-email-templates/templates/action",
        "subject": "Action email subject"
    },
    "alert": {
        "template": "transactional-email-templates/templates/alert",
        "subject": "Alert email subject"
    },
    
    "billing": {
        "template": "transactional-email-templates/templates/billing",
        "subject": "Billing email subject"
    }
}

class MailManager(models.Manager):

    def create_mail(self, template, subject, context, to_address, from_address=None):
        """
            Create a Mail object with proper validation

            e.g.

            Mail.objects.create_mail("hello", "Hello world!",{'name': 'Jens'},"me@jensneuhaus.de")
        """

        if from_address is None:
            from_address = settings.DEFAULT_FROM_EMAIL

        mail = self.create(subject=subject, template=template, context=context, from_address=from_address, to_address=to_address)
        return mail


class Mail(UUIDMixin):

    from_address = models.EmailField(
        _("Sender email address"),
        help_text=_("The 'from' field of the email"),
        null=False,
        blank=False
    )
    to_address = models.EmailField(
        _("Recipient email address"),
        help_text=_("The 'to' field of the email"),
        null=False,
        blank=False
    )

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

    subject = models.CharField(
        _("Email Subject line"),
        help_text=_("Subject line, saved after generating from context"),
        max_length=500,
        null=False,
        blank=False
    )
    context = models.TextField(
        _("Data of email context"),
        help_text=_("JSON dump of context dictionary used to fill in templates"),
        null=False,
        blank=False
    )

    time_queued = models.DateTimeField(
        _("Time mail was added to the send queue"),
        help_text=_("This is when send_async.. is called"),
        null=True,
        blank=True
    )
    time_sent = models.DateTimeField(
        _("Time mail was sent"),
        help_text=_("This is when mail.send is called"),
        null=True,
        blank=True
    )
    time_delivered = models.DateTimeField(
        _("Time mail was delivered"),
        help_text=_("This is given by the Mail sender"),
        null=True,
        blank=True
    )

    objects = MailManager()

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

        mail = cls(subject=subject, context=context, from_address=from_address, to_address=to_address)
        return mail

    def send(self,sendgrid_api=False):
        """
            Sends the mail using data from the Mail object

            Checks for existing template. Text is needed, HTML is optional.

            It can be called directly, but is usually called asynchronously.
         """

        template_name = MAIL_TEMPLATES[self.template]['template']
        subject_template = MAIL_TEMPLATES[self.template]['subject']

        try:
            txt_content = render_to_string(
                "mails/{}.txt".format(template_name),
                self.context
            )
        except TemplateDoesNotExist:
            raise ImportError(
                "Txt template not found: mails/{}.txt".format(template_name)
            )

        try:
            html_content = render_to_string(
                "mails/{}.html".format(template_name),
                self.context
            )
        except TemplateDoesNotExist:
            print(
                "HTML template not found: mails/{}.html".format(template_name)
            )
            html_content = None

        if sendgrid_api:

            data = {
                "personalizations": [
                    {
                        "to": [
                            {
                                "email": self.to_address
                            }
                        ],
                        "subject": self.subject
                    }
                ],
                "from": {
                    "email": self.from_address
                },
                "content": [
                    {
                        "type": "text/plain",
                        "value": txt_content
                    }
                ]
            }
            response = sg.client.mail.send.post(request_body=data)
            print("Email with UUID {} was sent with Sendgrid API.".format(self.id))

            print(response.status_code)
            print(response.body)
            print(response.headers)

        else:

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

