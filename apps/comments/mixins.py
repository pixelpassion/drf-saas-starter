from rest_framework.decorators import detail_route

from django.contrib.contenttypes.models import ContentType

from .views import CommentViewSet


class CommentsMixin:
    """A mixin to add commenting of objects to a ViewSet of a different app."""

    @detail_route(methods=['get', 'post'], url_path='comments')
    def comments(self, request, *args, **kwargs):
        """Call the appropriate view of the CommentViewSet."""
        kwargs['content_type'] = ContentType.objects.get_for_model(self.queryset.model)
        if request.method == 'GET':
            return CommentViewSet.as_view({'get': 'list'})(request, *args, **kwargs)
        elif request.method == 'POST':
            return CommentViewSet.as_view({'post': 'create'})(request, *args, **kwargs)
