from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView, RedirectView
from django.conf.urls.static import static
from django.conf import settings
from django.core.urlresolvers import reverse_lazy

urlpatterns = [

    url(r'^$', TemplateView.as_view(template_name='pages/home.html'), name='home'),
    url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name='about'),
    url(r'^dashboard/$', TemplateView.as_view(template_name='pages/dashboard.html'), name='dashboard'),

    url(r'^admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name='index.html')),

    url(r'^users/', include('apps.users.urls', namespace='users')),
    url(r'^accounts/', include('allauth.urls')),

    url(r'^crossdomain\.xml$', RedirectView.as_view(url=settings.STATIC_URL + 'crossdomain.xml')),

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]