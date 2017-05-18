# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework import viewsets
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model

from ..comments.mixins import CommentsMixin
from .models import User
from .serializers import UserSerializer


class UserViewSet(CommentsMixin, viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
