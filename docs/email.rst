
******************
E-Mail
******************

Sending mails
--------------------

In development
==============

We are using a Docker container for `Mailhog <https://github.com/mailhog/MailHog>`_.

It will accept SMTP mails via ``localhost:1025`` and provide a Weboverview for mails at http://127.0.0.1:8025/

In production
==============

django-saas-starter uses django-anymail to stay flexible, it uses the `Sendgrid <https://www.sendgrid.com/>`_ adapter but it can be switched for Mailgun etc.

For Sendgrid you need to set::

    EMAIL_BACKEND="anymail.backends.sendgrid.SendGridBackend"
    SENDGRID_API_KEY="<your_sendgrid_api_key"

You will get an error if you are not setting the SENDGRID_API_KEY::

    AnymailRequestsAPIError at /api/password/reset/
    Sending a message to newuser@example.org from mail@example.org
    SendGrid API response 401:
    {
      "errors": [
        {
          "message": "The provided authorization grant is invalid, expired, or revoked",
          "field": null,
          "help": null
        }
      ]
    }



Dynamic mail templates
----------------------

* which templates? what are they doing?
* how can they be changed?

Saving mails
--------------------

* All mails are saved in the admin
* tracking status is shown
