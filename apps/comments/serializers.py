from rest_framework.serializers import ModelSerializer

from .models import Comment


class CommentSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ('content_type', 'object_id', 'author', 'content', 'time_created')
        read_only_fields = ('time_created',)
