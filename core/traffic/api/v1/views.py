# Django Imports
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

# Third-Party Imports
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from traffic.api.v1.services.graph_service import GraphService
from drf_spectacular.utils import extend_schema

# Locale Imports
from .serializers import CreateTrafficSerializer, CameraTrafficSerializer, CarTrackingViewSerializer
from traffic.models import TrafficLogs
from .services.graph_service import GraphService
from datetime import datetime
import time

class CreateTrafficLogView(CreateAPIView):
    serializer_class = CreateTrafficSerializer
    permission_classes = [IsAuthenticated,]

class CreateCameraView(CreateAPIView):
    serializer_class = CameraTrafficSerializer
    permission_classes = [IsAuthenticated,]
    
class CarTrackingView(ListAPIView):  
    serializer_class = CarTrackingViewSerializer
    @extend_schema(
            parameters=[CarTrackingViewSerializer],
    )
    def get(self, request):
        serializer = self.serializer_class(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        start_time = time.time()
        
        graph_service = GraphService()
        
        
        plate_number = serializer.validated_data.get("plate_number")
        page_number = serializer.validated_data["page_number"]
        limit = serializer.validated_data["limit"]
        
        if plate_number is not None:
            try:
                page_number = int(page_number) if page_number else 1
                limit = int(limit) if limit else 10
            except ValueError:
                return Response(
                    {"error": "page_number و limit باید عدد باشند"},
                    status=400
                )
            
            tracking = graph_service.get_traffic_by_plate_number_path(
                plate_number, page_number, limit
            )

            if not tracking:
                return Response(
                    {"error": "خودرو یافت نشد یا ترددی ثبت نشده است"}, 
                    status=404
                )
       
        else:
            tracking = graph_service.get_traffic_by_plate_number_path(
                None, page_number, limit
            )

            
        end_time = time.time()
        full_time = end_time - start_time 
        time_formatted = str(datetime.utcfromtimestamp(full_time).strftime('%M:%S.%f'))[:-3]
        return Response({"path": tracking, "full_time":time_formatted})
class CarTrackingView1(ListAPIView):   
    def get(self, request):
        path_details = GraphService()
        tracking = path_details.delete_all_data()
        return Response({
            "path": tracking
        })

class SuspiciousVehiclesNeo4jAPIView(ListAPIView):
    def get(self, request, page_number, limit):
        start_time = time.time()
        graph_service = GraphService()
        tracking = graph_service.get_suspicious_vehicles(
            page_number, limit
        )
        end_time = time.time()
        full_time = start_time - end_time 
        return Response({"path": tracking, "full_time":full_time})


class GettingTrafficLogsAll(ListAPIView):
    cache_response_timeout = 60 * 1
    def get(self, request, page_number, limit):
        start_time = time.time()
        graph_service = GraphService()
        tracking = graph_service.get_all_traffic_logs(page_number, limit)
        end_time = time.time()
        full_time = end_time - start_time 
        time_formatted = str(datetime.utcfromtimestamp(full_time).strftime('%M:%S.%f'))[:-3]
        return Response({"path": tracking, "full_time":time_formatted})
