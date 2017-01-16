from django.contrib.sites.models import Site
from apps.users.models import User
from allauth.account.adapter import get_adapter
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template import TemplateDoesNotExist
from django.template.loader import render_to_string
from main.celery import app
from sendgrid.helpers.mail import *
import sendgrid
from django.conf import settings


@app.task(bind=True)
def send_sendgrid_mail(self, context_dict):
    """
    From the anymail class, would be better to use the class
    """

    if not settings.SENDGRID_API_KEY:
        raise NotImplementedError("No SENDGRID_API_KEY set")

    sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)
    from_email = Email("me@jensneuhaus.de")
    to_email = Email("kontakt@jensneuhaus.de")
    subject = "Sending with SendGrid is Fun: %s" % context_dict['number']
    content = Content("text/plain", "and easy to do anywhere, even with Python")
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)


@app.task(bind=True)
def send_anymail_mail(self, context_dict):

    msg = EmailMultiAlternatives("Subject %s" % context_dict['number'],
                                 "text body",
                                 "from@example.com",
                                 ["me@jensneuhaus.de"]
                                 )
    msg.attach_alternative("<html>html body</html>", "text/html")
    msg.send()


    # email = context_dict["email"]
    # template_prefix = context_dict["template_prefix"]
    #
    # context = {
    #     'current_site': Site.objects.get(id=int(context_dict["current_site"])),
    #     'activate_url': context_dict["activate_url"],
    #     'key': context_dict["key"],
    #     'user': User.objects.get(id=int(context_dict["user"]))
    # }
    #
    # subject = render_to_string('{0}_subject.txt'.format(template_prefix), context)
    # # remove superfluous line breaks
    # subject = " ".join(subject.splitlines()).strip()
    # subject = get_adapter().format_email_subject(subject)
    #
    # from_email = get_adapter().get_from_email()
    #
    # bodies = {}
    # for ext in ['html', 'txt']:
    #     try:
    #         template_name = '{0}_message.{1}'.format(template_prefix, ext)
    #         bodies[ext] = render_to_string(template_name,
    #                                        context).strip()
    #     except TemplateDoesNotExist:
    #         if ext == 'txt' and not bodies:
    #             # We need at least one body
    #             raise
    # if 'txt' in bodies:
    #     msg = EmailMultiAlternatives(subject,
    #                                  bodies['txt'],
    #                                  from_email,
    #                                  [email])
    #     if 'html' in bodies:
    #         msg.attach_alternative(bodies['html'], 'text/html')
    # else:
    #     msg = EmailMessage(subject,
    #                        bodies['html'],
    #                        from_email,
    #                        [email])
    #     msg.content_subtype = 'html'  # Main content is now text/html
    #
    # msg.send()
