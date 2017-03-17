from django.conf import settings
from django.test import TestCase
from .models import Mail


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

        
class SendMailTest(TestCase):

    def setUp(self):
        valid_args = {
            "template": "alert",
            "context": {
                "business_name": "Business Name", 
                "alert_warning": "Alert message from CompanyName", 
                "recipient_name": "John Doe",
                "content": [
                    {"text": "Lorem ipsum dolor sit amet. This is a sentence."}, 
                    {"text": "Example Button", 
                     "link": "https://www.example.com/"},
                    {"text": "Lorem ipsum dolor sit amet."}
                ]
            }, 
            "to_address": "serious.insomnia@gmail.com",
            "from_address": "mail-test@mailtest.com",
            "subject": "Hello there"
        }
        
        # Create valid Mail object
        self.mail = Mail.objects.create_mail(
            valid_args["template"],
            valid_args["context"],
            valid_args["to_address"]
        )

        # Save UUID for later
        self.mail_uuid = self.mail.id
    
    def test_send_mail_directly(self):
        pass

    def test_send_mail_asynchronous(self):
        pass

    def test_send_mail_with_db_errors(self):
        # Test: Pass nonexistent UUID, should raise AttributeError
        pass

    def test_send_mail_with_template_errors(self):
        # Missing required template field
        pass
