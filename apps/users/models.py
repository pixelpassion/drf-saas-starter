# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.utils import timezone

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email address'),
                              help_text=_("A valid user email"),
                              null=False, blank=False, unique=True)

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

    USERNAME_FIELD = 'email'

    #objects = EmailUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        permissions = (
            ("can_read_swagger_docs", "Can read swagger docs"),
        )

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'email': self.email})
