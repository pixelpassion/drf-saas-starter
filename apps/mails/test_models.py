from datetime import timedelta

from django.conf import settings
from django.test import TestCase, override_settings
from django.utils import timezone
from .models import Mail, MailTemplate
from urllib.error import HTTPError
from django.utils import timezone


class CreateMailTest(TestCase):

    def setUp(self):
        self.valid_template = "alert"
        self.valid_to_address = "serious.insomnia@gmail.com"
        self.valid_from_address = "mail-test@mailtest.com"
        self.valid_subject = "Hello there"
        self.valid_context = {
            "business_name": "Business Name", 
            "alert_warning": "Alert message from CompanyName", 
            "recipient_name": "John Doe",
            "content": [
                {"text": "Lorem ipsum dolor sit amet. This is a sentence."}, 
                {"text": "Example Button", 
                 "link": "https://www.example.com/"},
                {"text": "Lorem ipsum dolor sit amet."}
            ]
        }

    def create_mail(self, template=None, context=None, to_address=None,
                    from_address="Default", subject="Default"):
        """Creates and returns Mail object with default valid fields"""
        
        return Mail.objects.create_mail(
            template if template else self.valid_template,
            context if context else self.valid_context,
            to_address if to_address else self.valid_to_address,
            from_address if from_address is not "Default" else self.valid_from_address,
            subject if subject is not "Default" else self.valid_subject
        )
    
    def test_create_mail_with_required_fields_only(self):
        """Call Mail.objects.create_mail with valid required arguments should succeed
        """
        
        mail_with_required_fields_only = self.create_mail(from_address=None, subject=None)

        # Make sure arguments were recorded correctly
        self.assertEqual(mail_with_required_fields_only.template, self.valid_template)
        self.assertEqual(mail_with_required_fields_only.context, self.valid_context)
        self.assertEqual(mail_with_required_fields_only.to_address, self.valid_to_address)

        # From address should be the default
        self.assertEqual(mail_with_required_fields_only.from_address, settings.DEFAULT_FROM_EMAIL)

        # Subject should be set to None
        self.assertIsNone(mail_with_required_fields_only.subject)
        
    def test_create_mail_with_optional_fields(self):
        """Call Mail.objects.create_mail with optional arguments should succeed
        """
        
        mail_with_optional_fields = self.create_mail()
        
        # Make sure arguments were recorded correctly
        self.assertEqual(mail_with_optional_fields.template, self.valid_template)
        self.assertEqual(mail_with_optional_fields.context, self.valid_context)
        self.assertEqual(mail_with_optional_fields.to_address, self.valid_to_address)
        self.assertEqual(mail_with_optional_fields.from_address, self.valid_from_address)
        self.assertEqual(mail_with_optional_fields.subject, self.valid_subject)

    def test_create_mail_with_invalid_template(self):
        """Call Mail.objects.create_mail with invalid template should fail."""
        
        with self.assertRaises(ValueError, msg="Invalid template name should raise ValueError"):
            self.create_mail(template="really bad template name")

    def test_create_mail_with_invalid_context(self):
        """Call Mail.objects.create_mail with invalid context should fail."""
        
        # Invalid context should raise ValueError
        with self.assertRaises(ValueError, msg="Invalid context should raise ValueError"):
            self.create_mail(context="Not a dictionary")
    
    def test_create_mail_with_invalid_to_address(self):
        """Call Mail.objects.create_mail with invalid to_address should fail"""
        
        with self.assertRaises(ValueError, msg="Invalid to address should raise ValueError"):
            self.create_mail(to_address="invalid email address")

    def test_create_mail_with_invalid_from_address(self):
        """Call Mail.objects.create_mail with invalid from_address should fail"""
        
        with self.assertRaises(ValueError, msg="Invalid from address should raise ValueError"):
            self.create_mail(from_address="invalid email address")
        
    def tearDown(self):
        self.valid_template = None
        self.valid_to_address = None
        self.valid_from_address = None
        self.valid_subject = None
        self.valid_context = None


@override_settings(SENDGRID_API_KEY='test-api-key')
class SendMailTest(TestCase):

    def setUp(self):
        # Create valid Mail object
        self.mail = Mail.objects.create_mail("alert", {}, "mailtest@sink.sendgrid.net", "test@example.com")

    def test_send_mail_anymail(self):
        """Call mail.send() 
        Make sure mail is actually sent.
        """
        self.mail.send()

    def test_send_mail_sendgrid(self):
        """
            Call mail.send() using sendgrid API
            Make sure mail is actually sent.

            This should be mocked later, right now its checking for a 401 HttpError sent by CircleCI
             because the SENDGRID_API_KEY is wrong in circle.yml

            urllib.error.HTTPError: HTTP Error 401: Unauthorized
        """
        with self.assertRaises(HTTPError):
            self.mail.send(sendgrid_api=True)

    def tearDown(self):
        self.mail = None


class SendMailInfoTest(TestCase):

    def setUp(self): 
        # Create valid Mail object
        self.mail = Mail.objects.create_mail("alert", {}, "serious.insomnia@gmail.com", "mail-test@mailtest.com", subject="Custom subject")

        # Send the mail and record time sent
        self.mail.send()

    def test_send_mail_subject(self):
        """Check that correct subject is recorded.
        """
        self.assertEqual(self.mail.subject, "Custom subject", msg="Mail subject recorded incorrectly")

    def test_send_mail_date(self):
        """Check that correct sent datetime is recorded.
        """
        self.assertTrue((self.mail.time_sent - timezone.now()) < timedelta(seconds=2), msg="Mail time_sent recorded inaccurately")
        
    def tearDown(self):
        self.mail = None


class MailTemplateTest(TestCase):

    def setUp(self):
        # Create valid MailTemplate object
        self.mail_template = MailTemplate(
            name="name",
            subject="{} from {}", 
            html_template="<p><b>Hello</b>, {{ name }}!</p>",
        )
        self.subject_context = ["Greetings", "Company Name"]
        self.context = {'name': 'Cheryl'}

    def test_make_subject(self):
        """Check that the correct subject line is generated.
        """
        self.assertEqual(self.mail_template.make_subject(self.subject_context), "Greetings from Company Name", msg="Mail template generated incorrect subject")

    def test_make_output(self):
        """Check that the correct html and text output is produced when both templates are provided.
        """
        self.mail_template.text_template = "Hello, {{ name }}!"
        self.mail_template.save()
        
        self.assertEqual(self.mail_template.make_output(self.context)['html'], "<p><b>Hello</b>, Cheryl!</p>", msg="Mail template (with both template fields provided) generated incorrect HTML output")
        self.assertEqual(self.mail_template.make_output(self.context)['text'], "Hello, Cheryl!", msg="Mail template (with both template fields provided) generated incorrect text output")

    def test_make_output_html_only(self):
        """
        Check that html_to_text() produces correct output.
        Check that the correct html and text output is produced when only html template is provided.
        """
        pass #@TO-DO

    def tearDown(self):
        self.mail_template = None
