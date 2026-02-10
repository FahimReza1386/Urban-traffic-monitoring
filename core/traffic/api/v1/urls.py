# Django Imports
from django.urls import path

# Locale Imports
from . import views

urlpatterns = [
    path("traffic/log", views.CreateTrafficLogView.as_view(), name="traffic create log"),
    path("traffic/log/<str:plate_number>/", views.CarTrackingView.as_view(), name="path log"),
    path("camera/create", views.CreateCameraView.as_view(), name="camera create"),
]