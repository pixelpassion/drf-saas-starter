from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView, TemplateView

from .views import HomeView

from apps.notifications.views import NotificationCreateView, TestLoginAsUser
from django_nyt.urls import get_pattern


urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),

    url(r'^email-verified/$', TemplateView.as_view(template_name="email_verified.html"), name='email_verified'),

    # this url is used to generate email content
    url(r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        TemplateView.as_view(template_name="password_reset_confirm.html"),
        name='password_reset_confirm'),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^api/', include('apps.api.urls')),
    url(r'^tenant/', include('apps.tenants.urls', namespace="tenants")),

    url(r'^crossdomain\.xml$', RedirectView.as_view(url=settings.STATIC_URL + 'crossdomain.xml')),

    url(r'^htmltopdf/', include('apps.htmltopdf.urls')),

    url(r'^nyt/', get_pattern()),

    url(r'^create/$', NotificationCreateView.as_view(), name='create_notification'),
    url(r'^login-as/(?P<pk>\d+)/$', TestLoginAsUser.as_view(), name='login_as'),

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
