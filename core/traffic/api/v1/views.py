# Django Imports
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

# Third-Party Imports
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
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
        start_time = time.perf_counter()
        serializer = self.serializer_class(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        graph_service = GraphService()

        plate_number = serializer.validated_data.get("plate_number")
        page = serializer.validated_data["page"]
        per_page = serializer.validated_data["per_page"]
        type_id = serializer.validated_data.get("type_id")
        start_date = serializer.validated_data.get("start_date")
        end_date = serializer.validated_data.get("end_date")
        order_by = serializer.validated_data.get("order_by")
        
        if type_id is not None and int(type_id) <= 0:
            type_id = None
        
        if order_by not in ["ASC", "DESC"]:
            order_by = None
        

        tracking = graph_service.get_traffic_by_plate_number_path(
            plate_number if plate_number else None,
            page,
            per_page,
            type_id,
            start_date if start_date else None,
            end_date if end_date else None,
            order_by if order_by else None,
        )

        if not tracking:
            return Response(
                {"error": "خودرو یافت نشد یا ترددی ثبت نشده است"},
                status=404
            )

        run_time = round(time.perf_counter() - start_time, 6)

        return Response(
            {"result": tracking, "runtime": run_time},
            status=status.HTTP_200_OK
        )

  
class DeleteTraffic(ListAPIView):   
    def get(self, request):
        path_details = GraphService()
        tracking = path_details.delete_all_data()
        return Response({
            "data": tracking
        })

class SuspiciousTrafficLogView(ListAPIView):
      
    serializer_class = CarTrackingViewSerializer
    @extend_schema(
            parameters=[CarTrackingViewSerializer],
    )
    def get(self, request):
        start_time = time.perf_counter()
        serializer = self.serializer_class(data=request.query_params)
        serializer.is_valid(raise_exception=True)
                
        graph_service = GraphService()
        
        
        plate_number = serializer.validated_data.get("plate_number")
        page = serializer.validated_data["page"]
        per_page = serializer.validated_data["per_page"]
        type_id = serializer.validated_data["type_id"]
        
        if plate_number is not None:
            try:
                page = int(page) if page else 1
                per_page = int(per_page) if per_page else 10
            except ValueError:
                return Response(
                    {"error": "page و per_page باید عدد باشند"},
                    status=400
                )
            
            tracking = graph_service.get_suspicious_vehicles(
                plate_number, page, per_page, type_id
            )

            if not tracking:
                return Response(
                    {"error": "خودرو یافت نشد یا ترددی ثبت نشده است"}, 
                    status=404
                )
       
        else:
            tracking = graph_service.get_suspicious_vehicles(
                None, page, per_page
            )
        run_time = round(time.perf_counter() - start_time, 6)
        return Response({"result": tracking, "runtime":run_time}, status=status.HTTP_200_OK)
  