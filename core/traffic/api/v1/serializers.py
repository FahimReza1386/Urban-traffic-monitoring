# Third-Party Imports
from rest_framework import serializers

# Locale Imports
from traffic.models import TrafficLogs, Cameras

class CreateTrafficSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficLogs
        fields = ("id", "plate_number", "camera_id", "timestamp", "type_id")
        

class CameraTrafficSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cameras
        fields = ("id", "name")


class CarTrackingViewSerializer(serializers.Serializer):
    plate_number = serializers.CharField(required=False, allow_blank=True)
    page_number = serializers.IntegerField(required=False, default=1)
    limit = serializers.IntegerField(required=False, default=10)