# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework.routers import DefaultRouter

from django.conf.urls import include, url

from . import views

# # Here the comments are added manually by including them under the detail view.
# urlpatterns = [
#
#     url(
#         regex=r'^$',
#         view=views.UserViewSet.as_view({'get': 'list'}),
#         name='list'
#     ),
#
#     url(
#         r'^(?P<pk>[\w.@+-]+)/',
#         include([
#             url(
#                 r'^$',
#                 views.UserViewSet.as_view({'get': 'retrieve'}),
#                 name='detail'
#             ),
#             url(
#                 r'^comments/$',
#                 views.UserViewSet.as_view({'get': 'comments', 'post': 'comments'})
#             ),
#         ])
#     ),
#
# ]


# If we use a router the comments are added via the @detail_route decorator in the CommentsMixin.
# This means, that nothing has to be changed here.

router = DefaultRouter()

router.register(r'', views.UserViewSet)

urlpatterns = router.urls
