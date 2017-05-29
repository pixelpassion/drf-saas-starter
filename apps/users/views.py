from rest_framework.viewsets import ModelViewSet

from ..actstream_drf.mixins import ActivitiesMixin
from ..comments.mixins import CommentsMixin
from .models import User
from .serializers import UserSerializer


class UserViewSet(ActivitiesMixin, CommentsMixin, ModelViewSet):
    """A ViewSet for viewing and editing user instances."""
    serializer_class = UserSerializer
    queryset = User.objects.all()
