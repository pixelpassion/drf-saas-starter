from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView, RedirectView
from django.conf import settings
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token
from apps.registration.views import UserRegistrationView
from apps.letsencrypt.views import acme_challenge

urlpatterns = [

    # Static pages
    url(r'^$', TemplateView.as_view(template_name='pages/index.html'), name='home'),
    url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name='about'),
    url(r'^dashboard/$', TemplateView.as_view(template_name='pages/dashboard.html'), name='dashboard'),

    url(r'^admin/', admin.site.urls),

    url(r'^users/', include('apps.users.urls', namespace='users')),
    url(r'^accounts/', include('apps.authentication.urls')),

    # JSON Web Token handling
    url(r'^api/auth/', obtain_jwt_token),
    url(r'^api/verify/', verify_jwt_token),

    url(r'^api/authentication/', include('rest_auth.urls')),
    url(r'^api/registration/', include('apps.registration.urls')),
    url(r'^api/registration2/', UserRegistrationView.as_view(), name="register"),

    #url(r'^api/registration/', include('rest_auth.registration.urls')),
    url(r'^api/users/', include('apps.users.api_urls', namespace='api_users')),

    url(r'^api/docs/', include('rest_framework_docs.urls')),


    #permission_required('users.can_read_swagger_docs', login_url='/admin/login/')

    url(r'^crossdomain\.xml$', RedirectView.as_view(url=settings.STATIC_URL + 'crossdomain.xml')),

    url(r'.well-known/acme-challenge/(?P<token>.+)', acme_challenge),

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]