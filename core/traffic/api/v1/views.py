# Third-Party Imports
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from traffic.api.v1.services.graph_service import GraphService

# Locale Imports
from .serializers import CreateTrafficSerializer, CameraTrafficSerializer
from traffic.models import TrafficLogs
from .services.graph_service import GraphService
from .paginations import TrafficPagination

class CreateTrafficLogView(CreateAPIView):
    serializer_class = CreateTrafficSerializer
    permission_classes = [IsAuthenticated,]

class CreateCameraView(CreateAPIView):
    serializer_class = CameraTrafficSerializer
    permission_classes = [IsAuthenticated,]