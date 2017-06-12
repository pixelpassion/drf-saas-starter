from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User, UserTenantRelationship


class TenantInline(admin.TabularInline):
    model = UserTenantRelationship
    extra = 0


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class MyUserCreationForm(UserCreationForm):

    error_message = UserCreationForm.error_messages.update({
        'duplicate_username': 'This username has already been taken.'
    })

    class Meta(UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])


@admin.register(User)
class MyUserAdmin(AuthUserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    list_display = ('id', 'date_joined', 'signed_in', 'username', 'email', 'first_name', 'last_name',
                    'get_tenants', 'is_active', 'is_superuser')
    list_editable = ('username', 'first_name', 'last_name', 'email', 'is_active',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'signed_in', 'date_joined', )
    search_fields = ['first_name', 'last_name', 'username', 'email', ]
    ordering = ('date_joined', )

    inlines = (TenantInline,)

    def get_tenants(self, obj):
        return "\n".join([t.name for t in obj.tenants.all()])
