from django.contrib import admin


# Locale Imports
from .models import TrafficLogs, Cameras, SuspiciousVehicles


@admin.register(TrafficLogs)
class TrafficLogsAdmin(admin.ModelAdmin):
    list_display = ("id", "plate_number", "camera_id", "timestamp", "type_id")
    list_filter = ("type_id",)
    search_fields = ("plate_number", "type_id")
    
@admin.register(Cameras)
class CamerasAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("id", "name")

@admin.register(SuspiciousVehicles)
class SuspiciousVehiclesAdmin(admin.ModelAdmin):
    list_display = ("plate_number", "camera_id", "timestamp", "type_id")
    list_filter = ("type_id",)
    search_fields = ("plate_number", "type_id")