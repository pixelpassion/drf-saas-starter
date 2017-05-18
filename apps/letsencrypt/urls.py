from django.conf.urls import include, url

from .views import acme_challenge

urlpatterns = [

    url(r'.well-known/acme-challenge/(?P<token>.+)', acme_challenge),

]
