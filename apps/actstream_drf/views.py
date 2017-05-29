from actstream.models import Action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from .serializers import ActionSerializer


class ActivitiesViewSet(ReadOnlyModelViewSet):
    serializer_class = ActionSerializer
    queryset = Action.objects.all()

    def list(self, request, *args, **kwargs):
        """list as in DRF but filter the queryset with kwargs.

        The original list method doesn't forward any kwargs to the filter_queryset method,
        this is why we (have to) overwrite the whole thing.
        """
        queryset = self.queryset.filter(target_content_type=kwargs['content_type']).filter(target_object_id=kwargs['pk'])

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
