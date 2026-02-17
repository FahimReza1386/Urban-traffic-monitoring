# Django Imports
from django.urls import path

# Locale Imports
from . import views

urlpatterns = [
    path("log/create", views.CreateTrafficLogView.as_view(), name="traffic-create-log"),
    path("log/list", views.CarTrackingView.as_view(), name="path-log"),
    path("log/suspicious/list", views.SuspiciousTrafficLogView.as_view(), name="suspicious-traffic-log"),
    path("camera/create", views.CreateCameraView.as_view(), name="camera-create"),
    # path("log/delete/all", views.DeleteTraffic.as_view(), name="path log"),
    # path("log/get/all/    <int:page_number>/<int:limit>", views.GettingTrafficLogsAll.as_view(), name="path log"),
]