from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView, RedirectView
from django.conf.urls.static import static
from django.conf import settings
from django.core.urlresolvers import reverse_lazy

urlpatterns = [

    url(r'^$', RedirectView.as_view(url='/accounts/login/'), name='home'),


    url(r'^admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name='index.html')),

    url(r'^accounts/', include('allauth.urls')),

    url(r'^crossdomain\.xml$', RedirectView.as_view(url=settings.STATIC_URL + 'crossdomain.xml')),

]

