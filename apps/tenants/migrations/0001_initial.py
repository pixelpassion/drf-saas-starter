# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-16 11:14
from __future__ import unicode_literals

import django.contrib.sites.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(max_length=100, unique=True, validators=[django.contrib.sites.models._simple_domain_name_validator], verbose_name='domain name')),
                ('name', models.CharField(max_length=50, verbose_name='display name')),
            ],
            options={
                'ordering': ('domain',),
                'verbose_name': 'domain',
                'verbose_name_plural': 'domains',
            },
        ),
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=False, help_text='Designates whether this tenant should be treated as active. ', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, help_text='When did the user join?', verbose_name='date joined')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sites.Site')),
            ],
            options={
                'verbose_name': 'tenant',
                'verbose_name_plural': 'tenants',
            },
        ),
        migrations.AddField(
            model_name='domain',
            name='tenant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tenants.Tenant'),
        ),
    ]
