import json
import sendgrid
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.core.validators import validate_email
from django.core.exceptions import ValidationError, ImproperlyConfigured
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.db import models
from django.template import Template, TemplateDoesNotExist, Context
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from tinymce import models as tinymce_models

from main.mixins import UUIDMixin
from main.logging import logger

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
    "tenants/invite": {
        "template": "tenants/invite",
        "subject": "You are invited, {{name}}"
    },
    "account/email/email_confirmation_signup": {
        "template": "tenants/signup_email_confirmation",
        "subject": "Your registration at {{PROJECT_NAME}}"
    }

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

        if not isinstance(context, dict):
            raise ValueError("The given context is not a dictionary: {}".format(context))

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

    time_created = models.DateTimeField(
        _("Creation time"),
        help_text=_("When was the mail created?"),
        default=timezone.now
    )

    time_sent = models.DateTimeField(
        _("Sent time"),
        help_text=_("When was the mail send via the backend?"),
        null=True,
        blank=True
    )
    time_delivered = models.DateTimeField(
        _("Delivery time"),
        help_text=_("Actual delivery time by the email backend"),
        null=True,
        blank=True
    )

    used_backend = models.CharField(
        _("E-Mail Backend"),
        help_text=_("Which email backend was used for sending?"),
        null=True,
        blank=True,
        max_length=128
    )

    objects = MailManager()

    def __str__(self):
        return "%s to %s" % (self.template, self.to_address)

    @classmethod
    def get_extra_context(cls):

        return {
            'PROJECT_NAME': settings.PROJECT_NAME
        }

    def send(self, sendgrid_api=False):
        """
            Sends the mail using data from the Mail object

            Checks for existing template. Text is needed, HTML is optional.

            It can be called directly, but is usually called asynchronously with tasks.send_asynchronous_mail.

            sendgrid_api=True uses the sendgrid API directly (with bypassing django-anymail)
         """

        context = {
            **self.context,
            **Mail.get_extra_context()
        }

        logger.warning(context)

        try:
            template_name = MAIL_TEMPLATES[self.template]['template']
        except KeyError:
            raise ImproperlyConfigured("{} is not a valid Template name".format(self.template))

        try:
            txt_content = render_to_string(
                "{}{}.txt".format(MAIL_TEMPLATES_PREFIX, template_name),
                context
            )
        except TemplateDoesNotExist:
            raise ImportError("Txt template not found: {}{}.txt".format(MAIL_TEMPLATES_PREFIX, template_name))

        try:
            html_content = render_to_string(
                "{}{}.html".format(MAIL_TEMPLATES_PREFIX, template_name),
                context
            )
        except TemplateDoesNotExist:
            logger.warning("HTML template not found: {}{}.html".format(MAIL_TEMPLATES_PREFIX, template_name))
            html_content = None

        if self.subject:
            subject = self.subject
        else:
            subject = MAIL_TEMPLATES[self.template]['subject']

        rendered_subject = Template(subject).render(Context(context))

        if sendgrid_api:

            if not settings.SENDGRID_API_KEY:
                raise ImproperlyConfigured("No SENDGRID_API_KEY set.")

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
            logger.debug("Email with UUID {} was sent with Sendgrid API.".format(self.id))
            logger.debug("Response Status Code: {}, Body: {}, Headers: {}".format(response.status_code, response.body, response.headers))

            self.used_backend = "Sendgrid ({})".format(response.status_code)

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

            logger.info("Email with UUID {} was sent.".format(self.id))

            self.used_backend = settings.EMAIL_BACKEND

        self.time_sent = timezone.now()
        self.save()


class MailTemplate(models.Model):

    name = models.CharField(
        _("Template name"),
        help_text=_("Should be a small string"),
        max_length=100
    )
    
    subject = models.CharField(
        _("Email subject line template"),
        help_text=_("A python template string for email subject"), 
        max_length=200
    )
    
    # HTML field for the html
    html_template = tinymce_models.HTMLField(
        _("HTML template (required)"),
        help_text=_("Use django template syntax")
    )
    text_template = models.TextField(
        _("Text template (optional)"),
        help_text=_("If not provided, it is generated dynamically from the HTML template."),
        default=""
    )

    def make_subject(self, inputs):
        """ Given a list of values, fill in subject template with values and return result.
        """
        return self.subject.format(*inputs)

    def make_output(self, context):
        """ Fills in HTML and TXT template with context, and returns a dictionary containing the results as strings.
        If there is no TXT template stored, then a dynamically generated text-only version will be returned instead. 
        """
        context = Context(context)
        
        html_output = Template(self.html_template).render(context)

        if(self.text_template):
            text_output = Template(self.text_template).render(context)
        else:
            text_output = html_to_text(html_output)

        return {
            'html': html_output,
            'text': text_output
        }

    def html_to_text(self, html_string):
        """ Returns text generated from given HTML string. For internal use only. 
            Usage: After filling in html template with context, pass it to this method to create the text-only version.
        """
        
        #TO-DO- implement this method.
        return "html_to_text() was called."
