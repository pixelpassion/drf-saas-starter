# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^$', views.UserView.as_view(), name="users-list"),
    url(r'^login/$', views.LoginView.as_view(), name="login"),
    url(r'^reset-password/$', view=views.PasswordResetView.as_view(), name="reset-password"),
    url(r'^reset-password/confirm/$', views.PasswordResetConfirmView.as_view(), name="reset-password-confirm"),

    url(r'^change-password/$', view=views.ChangePasswordView.as_view(), name="change-password"),

    url(r'^current/$', views.UserProfileView.as_view(), name="profile"),

]
