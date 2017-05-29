from django.conf.urls import url

from .views import TenantDashboardView

urlpatterns = [

    url(
        regex=r'^dashboard/$',
        view=TenantDashboardView.as_view(),
        name='dashboard'
    ),
]
