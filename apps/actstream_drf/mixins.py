from rest_framework.decorators import detail_route

from django.contrib.contenttypes.models import ContentType

from .views import ActivitiesViewSet


class ActivitiesMixin:
    """A mixin to add an activity stream of objects to a ViewSet of a different app."""

    @detail_route(url_path='activities')
    def activities(self, request, *args, **kwargs):
        """Show the activity stream of the object this lies under."""
        kwargs['content_type'] = ContentType.objects.get_for_model(self.queryset.model)
        return ActivitiesViewSet.as_view({'get': 'list'})(request, *args, **kwargs)
