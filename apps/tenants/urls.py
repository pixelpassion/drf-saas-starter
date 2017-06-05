from django.conf.urls import url

from .views import TenantDashboardView

app_name = 'apps.tenants'
urlpatterns = [
    url(
        regex=r'^dashboard/$',
        view=TenantDashboardView.as_view(),
        name='dashboard'
    ),
]
