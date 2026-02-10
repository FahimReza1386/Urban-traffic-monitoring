# Third-Party Imports
from rest_framework import serializers

# Locale Imports
from traffic.models import TrafficLogs, Cameras

class CreateTrafficSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficLogs
        fields = ("plate_number", "camera_id", "timestamp", "type_id")
        
        
class CameraTrafficSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cameras
        fields = ("name",)
