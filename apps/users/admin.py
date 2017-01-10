# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _

from .models import User

#
# class MyUserChangeForm(UserChangeForm):
#     class Meta(UserChangeForm.Meta):
#         model = User
#
#
# class MyUserCreationForm(UserCreationForm):
#
#     error_message = UserCreationForm.error_messages.update({
#         'duplicate_email': 'This email has already been taken.'
#     })
#
#     class Meta(UserCreationForm.Meta):
#         model = User
#
#     def clean_email(self):
#         email = self.cleaned_data["email"]
#         try:
#             User.objects.get(email=email)
#         except User.DoesNotExist:
#             return email
#         raise forms.ValidationError(self.error_messages['duplicate_email'])


@admin.register(User)
class UserAdmin(AuthUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password', )}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),

    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('id', 'email', 'is_superuser', 'is_staff', 'is_active', )
    list_editable = ('is_active', )
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', )
    ordering = ('email',)
