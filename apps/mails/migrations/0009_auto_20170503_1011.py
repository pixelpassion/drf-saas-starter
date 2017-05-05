# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-03 10:11
from __future__ import unicode_literals

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('mails', '0008_auto_20170329_0948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailtemplate',
            name='html_template',
            field=tinymce.models.HTMLField(help_text="The HTML template, written with Django's template syntax; required", verbose_name='HTML template (required)'),
        ),
        migrations.AlterField(
            model_name='mailtemplate',
            name='name',
            field=models.CharField(help_text='Template name; a short all-lowercase string', max_length=100, verbose_name='Template name'),
        ),
        migrations.AlterField(
            model_name='mailtemplate',
            name='subject',
            field=models.CharField(help_text='A format string like "Hello {}"; required', max_length=200, verbose_name='Email subject line template'),
        ),
        migrations.AlterField(
            model_name='mailtemplate',
            name='text_template',
            field=models.TextField(blank=True, default='', help_text='This is an optional field for adding a custom text-only version of this template. If left blank, the plaintext email will be generated dynamically from the HTML when needed.', null=True, verbose_name='Text template (optional)'),
        ),
    ]