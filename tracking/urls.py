
from django.urls import path
from . import views as v
from django.contrib.auth.views import LogoutView

app_name = 'tracking'
urlpatterns = [
    path(
        'location/',
        v.AtualizarLocalizacaoAPIView.as_view(),
        name='tracking_location'
    ),
    path(
        'drivers/',
        v.DriversOnlineAPIView.as_view(),
        name='tracking-drivers'
    ),
    path(
        'tracking-dashboard/',
        v.TrackingDashboardView.as_view(),
        name='tracking-dashboard'
    ),
    path(
        'drivers/<int:entregador_id>/route/',
        v.DriverRouteAPIView.as_view(),
        name='tracking-driver-route'
),
]