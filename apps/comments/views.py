from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Comment
from .serializers import CommentSerializer


class CommentViewSet(ModelViewSet):
    """The ViewSet for comments where available information from the request will be integrated."""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def create(self, request, *args, **kwargs):
        """Add content_type, object_id and author to the comment."""
        self.request.data['content_type'] = kwargs['content_type'].pk
        self.request.data['object_id'] = str(kwargs['pk'])
        self.request.data['author'] = self.request.user.pk
        return super().create(self.request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """list as in DRF but filter the queryset with kwargs.

        The original list method doesn't forward any kwargs to the filter_queryset method,
        this is why we (have to) overwrite the whole thing.
        """
        queryset = self.queryset.filter(content_type=kwargs['content_type']).filter(object_id=kwargs['pk'])

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
