from rest_framework.decorators import detail_route

from django.contrib.contenttypes.models import ContentType

from .views import ActivityViewSet


class ActivityMixin:

    @detail_route(url_path='activity')
    def activity(self, request, *args, **kwargs):
        kwargs['content_type'] = ContentType.objects.get_for_model(self.queryset.model)
        return ActivityViewSet.as_view({'get': 'list'})(request, *args, **kwargs)
