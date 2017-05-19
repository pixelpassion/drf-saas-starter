from rest_framework import viewsets
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model

from ..actstream_drf.mixins import ActivityMixin
from ..comments.mixins import CommentsMixin
from .models import User
from .serializers import UserSerializer


class UserViewSet(ActivityMixin, CommentsMixin, viewsets.ModelViewSet):
    """A ViewSet for viewing and editing user instances."""
    serializer_class = UserSerializer
    queryset = User.objects.all()
