# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Mail


@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_address', 'to_address', 'template', 'subject', 'context', )
    search_fields = ['from_address', 'to_address', 'template', ]
