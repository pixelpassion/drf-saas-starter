from django.conf import settings
from django.test import TestCase
from .models import Mail

class CreateMailTest(TestCase):

    def setUp(self):
        self.valid_args = {
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

    
    def test_create_mail_with_valid_args(self):
        """Call Mail.objects.create_mail with valid arguments should succeed"""
        
        mail_with_required_args_only = Mail.objects.create_mail(
            self.valid_args["template"],
            self.valid_args["context"],
            self.valid_args["to_address"]
        )

        # Make sure arguments were recorded correctly
        self.assertEqual(mail_with_required_args_only.template,
                         self.valid_args["template"])
        self.assertEqual(mail_with_required_args_only.context,
                         self.valid_args["context"])
        self.assertEqual(mail_with_required_args_only.to_address,
                         self.valid_args["to_address"])

        # From address should be the default
        self.assertEqual(mail_with_required_args_only.from_address,
                         settings.DEFAULT_FROM_EMAIL)

        # Subject should be set to None
        self.assertIsNone(mail_with_required_args_only.subject)
                
        mail_with_optional_args = Mail.objects.create_mail(
            self.valid_args["template"],
            self.valid_args["context"],
            self.valid_args["to_address"],
            self.valid_args["from_address"],
            self.valid_args["subject"]
        )
        
        # Make sure arguments were recorded correctly
        self.assertEqual(mail_with_optional_args.template,
                         self.valid_args["template"])
        self.assertEqual(mail_with_optional_args.context,
                         self.valid_args["context"])
        self.assertEqual(mail_with_optional_args.to_address,
                         self.valid_args["to_address"])
        self.assertEqual(mail_with_optional_args.from_address,
                         self.valid_args["from_address"])
        self.assertEqual(mail_with_optional_args.subject,
                         self.valid_args["subject"])


    def test_create_mail_with_invalid_args(self):
        """Call Mail.objects.create_mail with invalid arguments should fail."""

        err_msg = "Invalid template name should raise ValueError"
        with self.assertRaises(ValueError, msg=err_msg):
            Mail.objects.create_mail(
                "really bad template name", 
                self.valid_args["context"],
                self.valid_args["to_address"]
            )

#        # Invalid context should raise ValueError
#        with self.assertRaises(ValueError):
#            Mail.objects.create_mail(
#                self.valid_args["template"],
#                ???,
#                self.valid_args["to_address"]
#            )

        err_msg = "Invalid to address should raise ValueError"
        with self.assertRaises(ValueError, msg=err_msg):
            Mail.objects.create_mail(
                self.valid_args["template"],
                self.valid_args["context"],
                "invalid email address"
            )

        err_msg = "Invalid from address should raise ValueError"
        with self.assertRaises(ValueError, msg=err_msg):
            Mail.objects.create_mail(
                self.valid_args["template"],
                self.valid_args["context"],
                self.valid_args["to_address"],
                "invalid email address"
            )

        
    def tearDown(self):
        self.valid_args = None



        
class SendMailTest(TestCase):

    def setUp(self):
        pass
    
    def test_send_mail_directly(self):
        pass

    def test_send_mail_asynchronous(self):
        pass

    def test_send_mail_with_db_errors(self):
        pass

    def test_send_mail_with_template_errors(self):
        pass
