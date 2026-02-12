# Django Imports
from django.urls import path

# Locale Imports
from . import views

urlpatterns = [
    path("log/create", views.CreateTrafficLogView.as_view(), name="traffic create log"),
    path("log/list/", views.CarTrackingView.as_view(), name="path log"),
    path("camera/create", views.CreateCameraView.as_view(), name="camera create"),
    # path("log/get/suspicious-vehicles/<int:page_number>/<int:limit>", views.SuspiciousVehiclesNeo4jAPIView.as_view(), name="suspicious-vehicles log"),
    # path("log/delete/all", views.CarTrackingView1.as_view(), name="path log"),
    # path("log/get/all/    <int:page_number>/<int:limit>", views.GettingTrafficLogsAll.as_view(), name="path log"),
]  