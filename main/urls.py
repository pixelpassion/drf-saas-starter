from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView, TemplateView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="home.html"), name='home'),

    url(r'^email-verified/$', TemplateView.as_view(template_name="email_verified.html"), name='email_verified'),

    # url(r'^signup/$', TemplateView.as_view(template_name="signup.html"),
    #     name='signup'),
    # url(r'^email-verification/$',
    #     TemplateView.as_view(template_name="email_confirm.html"),
    #     name='email-verification'),
    # url(r'^login/$', TemplateView.as_view(template_name="login.html"),
    #     name='login'),
    # url(r'^logout/$', TemplateView.as_view(template_name="logout.html"),
    #     name='logout'),
    # url(r'^password-reset/$',
    #     TemplateView.as_view(template_name="password_reset.html"),
    #     name='password-reset'),
    # url(r'^password-reset/confirm/$',
    #     TemplateView.as_view(template_name="password_reset_confirm.html"),
    #     name='password-reset-confirm'),
    #
    # url(r'^user-details/$',
    #     TemplateView.as_view(template_name="user_details.html"),
    #     name='user-details'),
    # url(r'^password-change/$',
    #     TemplateView.as_view(template_name="password_change.html"),
    #     name='password-change'),


    # this url is used to generate email content
    url(r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        TemplateView.as_view(template_name="password_reset_confirm.html"),
        name='password_reset_confirm'),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^api/', include('apps.api.urls', namespace="api")),
    url(r'^tenant/', include('apps.tenants.urls', namespace="tenants")),

    url(r'^crossdomain\.xml$', RedirectView.as_view(url=settings.STATIC_URL + 'crossdomain.xml')),
    url(r'^', include('apps.letsencrypt.urls', namespace="letsencrypt")),

    # Account handling from allauth, probably not needed in an API based backend, TODO: Delete
    # url(r'^account/', include('allauth.urls')),


    url(r'^htmltopdf/', include('apps.htmltopdf.urls')),


]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
