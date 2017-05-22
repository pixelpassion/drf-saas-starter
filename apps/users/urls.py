from rest_framework.routers import DefaultRouter

from django.conf.urls import include, url

from .views import UserViewSet


# Here the comments and activity is added manually by including them under the detail view.

# urlpatterns = [
#
#     url(
#         regex=r'^$',
#         view=UserViewSet.as_view({'get': 'list'}),
#         name='list'
#     ),
#
#     url(
#         r'^(?P<pk>[\w.@+-]+)/',
#         include([
#             url(
#                 r'^$',
#                 UserViewSet.as_view({'get': 'retrieve'}),
#                 name='detail'
#             ),
#             url(
#                 r'^comments/$',
#                 UserViewSet.as_view({'get': 'comments', 'post': 'comments'})
#             ),
#             url(
#                 r'^activity/$',
#                 UserViewSet.as_view({'get': 'activity'})
#             ),
#         ])
#     ),
#
# ]


# If we use a router the comments and activity is added via
# the @detail_route decorator in the CommentsMixin and ActivityMixin.
# This means, that nothing has to be changed here.


router = DefaultRouter()
router.register(r'', UserViewSet)
urlpatterns = router.urls
