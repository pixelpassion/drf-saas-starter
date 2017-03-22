from django.contrib import admin
from .models import Tenant, Domain
from django.contrib.sites.models import Site


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

