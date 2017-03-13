# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Mail
from django.utils.translation import ugettext_lazy as _
from .tasks import send_asynchronous_mail


@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):

    def send_mail_now(self, request, queryset):

        mails_sent = 0

        for object in queryset:
            send_asynchronous_mail(str(object.id))
            mails_sent += 1

        if mails_sent == 1:
            message_bit = _("1 Mail was")
        else:
            message_bit = _("%s Mails were") % mails_sent
        self.message_user(request, "%s sent" % message_bit)

    send_mail_now.short_description = "Send mail now"

    list_display = ('id', 'from_address', 'to_address', 'template', 'subject', 'context', )
    search_fields = ['from_address', 'to_address', 'template', ]

    actions = [send_mail_now, ]
