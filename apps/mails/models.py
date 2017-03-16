import json
import sendgrid

from django.conf import *
from django.contrib.postgres.fields import JSONField
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.db import models
from django.template import Template, TemplateDoesNotExist, Context
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from apps.tenants.models import TenantMixin
from main.mixins import UUIDMixin

if not settings.SENDGRID_API_KEY:
    raise NotImplementedError("No SENDGRID_API_KEY set")

sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)

MAIL_TEMPLATES_PREFIX = "mails/"

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
    },
    "hello": {
        "template": "hello",
        "subject": "Hello World, {{name}}"
    },
}


class MailManager(models.Manager):

    def create_mail(self, template, context, to_address, from_address=None, subject=None):
        """
            Create a Mail object with proper validation

            e.g.

            mail = Mail.objects.create_mail("hello", {'name': 'Jens'},"me@jensneuhaus.de")
            mail.send()

        """

        try:
            MAIL_TEMPLATES[template]
        except KeyError:
            raise ValueError("{} is not a valid Template name".format(template))

        try:
            context_string = json.dumps(context)
            context_json = json.loads(context_string)
        except ValueError:
            raise ValueError("The given context is not valid: {}".format(context))

        if from_address is None:
            from_address = settings.DEFAULT_FROM_EMAIL

        try:
            validate_email(from_address)
        except ValidationError:
            raise ValueError("The given email is not valid: {}".format(from_address))

        try:
            validate_email(to_address)
        except ValidationError:
            raise ValueError("The given email is not valid: {}".format(to_address))

        mail = self.create(template=template, context=context_json, from_address=from_address, to_address=to_address, subject=subject)
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
        help_text=_("Subject line for a mail"),
        max_length=500,
        null=True,
        blank=True
    )
    context = JSONField(
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

    def send(self, sendgrid_api=False):
        """
            Sends the mail using data from the Mail object

            Checks for existing template. Text is needed, HTML is optional.

            It can be called directly, but is usually called asynchronously with tasks.send_asynchronous_mail.

            sendgrid_api=True uses the sendgrid API directly (with bypassing django-anymail)
         """

        try:
            template_name = MAIL_TEMPLATES[self.template]['template']
        except KeyError:
            raise ImproperlyConfigured("{} is not a valid Template name".format(self.template))

        try:
            txt_content = render_to_string(
                "{}{}.txt".format(MAIL_TEMPLATES_PREFIX, template_name),
                self.context
            )
        except TemplateDoesNotExist:
            raise ImportError("Txt template not found: {}{}.txt".format(MAIL_TEMPLATES_PREFIX, template_name))

        try:
            html_content = render_to_string(
                "{}{}.html".format(MAIL_TEMPLATES_PREFIX, template_name),
                self.context
            )
        except TemplateDoesNotExist:
            print("HTML template not found: {}{}.html".format(MAIL_TEMPLATES_PREFIX, template_name))
            html_content = None

        if self.subject:
            subject = self.subject
        else:
            subject = MAIL_TEMPLATES[self.template]['subject']

        rendered_subject = Template(subject).render(Context(self.context))

        if sendgrid_api:

            data = {
                "personalizations": [
                    {
                        "to": [
                            {
                                "email": self.to_address
                            }
                        ],
                        "subject": rendered_subject
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
                    rendered_subject,
                    txt_content,
                    self.from_address,
                    [self.to_address]
                )
                msg.attach_alternative(html_content, "text/html")

            else:
                msg = EmailMessage(
                    rendered_subject,
                    txt_content,
                    self.from_address,
                    [self.to_address]
                )

            msg.send()

            print("Email with UUID {} was sent.".format(self.id))

