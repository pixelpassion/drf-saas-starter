from actstream.models import Action
from rest_framework.serializers import ModelSerializer, RelatedField

from ..comments.models import Comment
from ..comments.serializers import CommentSerializer
from ..users.models import User
from ..users.serializers import UserSerializer


class ActionObjectGenericRelatedField(RelatedField):
    """A custom field to use for the generic relationships of Action."""

    def to_representation(self, value):
        """Choose the right serializer for an object."""
        if isinstance(value, User):
            serializer = UserSerializer(value)
        elif isinstance(value, Comment):
            serializer = CommentSerializer(value)
        else:
            raise Exception("Serializer of object type is not defined")  # FIXME how do we want to handle it like this?
        return serializer.data


class ActionSerializer(ModelSerializer):
    """A serializer for Action where the usage of Generic Foreign Keys is taken care of."""
    actor = ActionObjectGenericRelatedField(read_only=True)
    action_object = ActionObjectGenericRelatedField(read_only=True)
    target = ActionObjectGenericRelatedField(read_only=True)

    class Meta:
        model = Action
        fields = ('actor', 'verb', 'action_object', 'target', 'timestamp')
