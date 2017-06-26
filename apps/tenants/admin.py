from django.contrib import admin
from django.utils.translation import ugettext as _

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
    list_display = ('id', 'name', 'site', 'is_active', 'date_joined', )
    list_editable = ('name', 'is_active')
    search_fields = ('name', )


@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    """Show invitations and give the admin the chance to send an invite."""
    list_display = ('tenant', 'first_name', 'last_name', 'email', )
    search_fields = ('tenant', 'first_name', 'last_name', 'email', )
    actions = ['send_invite']

    def send_invite(self, request, queryset):

        rows_updated = 0

        for invite in queryset:
            invite.send_invite()
            rows_updated += 1

        if rows_updated == 1:
            message = _("1 Invite was sent.")
        else:
            message = _("%s Invites were sent.") % rows_updated
        self.message_user(request, message)

    send_invite.short_description = _("Send an invite")
