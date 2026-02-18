# Third-Party Imports
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

# Locale Imports
from .serializers import (
    CreateTrafficSerializer,
    CameraTrafficSerializer,
    CarTrackingViewSerializer,
)
from .services.graph_service import GraphService
import time


class CreateTrafficLogView(CreateAPIView):
    """
    A View For Create TrafficLogs in api ..
    """

    serializer_class = CreateTrafficSerializer
    permission_classes = [
        IsAuthenticated,
    ]


class CreateCameraView(CreateAPIView):
    """
    A View For Create Camera in api ..
    """

    serializer_class = CameraTrafficSerializer
    permission_classes = [
        IsAuthenticated,
    ]


class CarTrackingView(ListAPIView):
    """
    To get the car route based on multiple inputs or the last few traffics
    """

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
                {"error": "خودرو یافت نشد یا ترددی ثبت نشده است"}, status=404
            )

        run_time = round(time.perf_counter() - start_time, 6)

        return Response(
            {"result": tracking, "runtime": run_time}, status=status.HTTP_200_OK
        )


class DeleteTraffic(ListAPIView):
    """
    A View For Deleting All Database When Changing the structure db ..
    """

    def get(self, request):
        path_details = GraphService()
        tracking = path_details.delete_all_data()
        return Response({"data": tracking})


class SuspiciousTrafficLogView(ListAPIView):
    """
    To get the suspicious vehicle's route based on multiple entries or the last few traffic
    """

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
                {"error": "خودرو یافت نشد یا ترددی ثبت نشده است"}, status=404
            )
        run_time = round(time.perf_counter() - start_time, 6)
        return Response(
            {"result": tracking, "runtime": run_time}, status=status.HTTP_200_OK
        )
