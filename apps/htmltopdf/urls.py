from django.conf.urls import url

from .views import example

urlpatterns = [
    url(r'^example/$', example, name='htmltopdf_example')
]
