from django.contrib import admin
from django.contrib.sites.models import Site

from .models import Domain, Invite, Tenant


class DomainInline(admin.TabularInline):
    model = Domain
    extra = 0


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'domain', 'name')
    search_fields = ('tenant', 'domain', 'name')


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'site', 'is_active', 'date_joined' )
    list_editable = ('name', 'is_active')
    search_fields = ('name', )


@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    """
        Show invitations and gives the admin the chance to send an invite.
    """

    # TODO: #63 - Show the status of the invitation (clicked, used) and the date/time of the sending

    def send_invite(self, request, queryset):

        rows_updated = 0

        for object in queryset:
            object.send_invite()
            rows_updated += 1

        if rows_updated == 1:
            message_bit = "1 Invite was"
        else:
            message_bit = "%s Invites were" % rows_updated
        self.message_user(request, "%s sent." % message_bit)

    send_invite.short_description = "Sent an invite"

    list_display = ('tenant', 'first_name', 'last_name', 'email', )
    search_fields = ('tenant', 'first_name', 'last_name', 'email', )
    actions = [send_invite, ]
