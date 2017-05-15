# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [

    url(
        regex=r'^$',
        view=views.UserViewSet.as_view({'get': 'list'}),
        name='list'
    ),

    url(
        regex=r'^(?P<pk>[\w.@+-]+)/$',
        view=views.UserViewSet.as_view({'get': 'retrieve'}),
        name='detail'
    ),

]