from django.urls import re_path
from .consumers import DriverTrackingConsumer

websocket_urlpatterns = [
    re_path(
        r'ws/tracking/drivers/$',
        DriverTrackingConsumer.as_asgi()
    ),
]