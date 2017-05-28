# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from django import forms


class NotificationCreateForm(forms.Form):

    name = forms.CharField(label="Message")

    class Meta:
        fields = ('name', )