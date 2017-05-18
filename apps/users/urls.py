# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework.routers import DefaultRouter

from .views import UserViewSet

# Here the comments are added manually by including them under the detail view.

# from django.conf.urls import include, url
# from .views import UserViewSet, CurrentUserView
#
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
#         ])
#     ),
#
# ]


# If we use a router the comments are added via the @detail_route decorator in the CommentsMixin.
# This means, that nothing has to be changed here.


router = DefaultRouter()
router.register(r'', UserViewSet)
urlpatterns = router.urls
