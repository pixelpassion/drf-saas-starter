# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def forwards_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    MailTemplate = apps.get_model("mails", "MailTemplate")
    db_alias = schema_editor.connection.alias
    MailTemplate.objects.using(db_alias).bulk_create([
        MailTemplate(name="hello", html_template="<p>Hello</p>"),
        MailTemplate(name="invite", html_template="<p>Invite</p>"),
        MailTemplate(name="email_confirmation_signup", html_template="<a href='{{ activation_url }}'>Confirm email address</a"),
    ])


def reverse_func(apps, schema_editor):
    # forwards_func() creates two Country instances,
    # so reverse_func() should delete them.
    MailTemplate = apps.get_model("mails", "MailTemplate")
    db_alias = schema_editor.connection.alias
    MailTemplate.objects.using(db_alias).filter(name="hello").delete()
    MailTemplate.objects.using(db_alias).filter(name="invite").delete()
    MailTemplate.objects.using(db_alias).filter(name="email_confirmation_signup").delete()


class Migration(migrations.Migration):

    dependencies = [
        ('mails', '0010_remove_mail_template'),
    ]
    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]