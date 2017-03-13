# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin)

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.validators import ASCIIUsernameValidator, UnicodeUsernameValidator
from django.utils import six, timezone
from main.mixins import UUIDMixin


class UserManager(BaseUserManager):
    use_in_migrations = True

    def find_next_available_username(self, wanted_username):
        counter = 1
        checked_username = wanted_username

        while True:

            try:
                self.model.objects.get(username=checked_username)
            except self.model.DoesNotExist:
                return checked_username

            counter += 1

            checked_username = "{}{}".format(wanted_username, counter)

    def _create_user(self, email, password, username=None, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not email:
            raise ValueError('The email must be set')

        email = self.normalize_email(email)

        if username is None or username == '':
            username = self.find_next_available_username(email.split("@")[0])

        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)

        return self._create_user(email, password, username, **extra_fields)

    def create_superuser(self, email, password, username=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, username, **extra_fields)


class User(AbstractBaseUser, UUIDMixin, PermissionsMixin):

    email = models.EmailField(_('email address'),
                              help_text=_("A valid user email"),
                              null=False, blank=False, unique=True)

    username_validator = UnicodeUsernameValidator() if six.PY3 else ASCIIUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    first_name = models.CharField(_('first name'),
                                  help_text=_("The first Name of the user"),
                                  max_length=30,
                                  blank=True
                                  )
    last_name = models.CharField(_('last name'),
                                 max_length=30,
                                 blank=True,
                                 help_text=_("The last Name of the user")
                                 )
    activation_token = models.CharField(_('activation_token'),
                                        help_text=_("The activation token of the user"),
                                        max_length=100, blank=True)

    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    date_joined = models.DateTimeField(_('date joined'), help_text=_("When did the user join?"), default=timezone.now)

    unneeded_field_to_test_correct_migrations = models.BooleanField(
        default=False
    )
    USERNAME_FIELD = 'email'

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.username

    def get_short_name(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})
