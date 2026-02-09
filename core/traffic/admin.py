from django.contrib import admin


# Locale Imports
from .models import TrafficLogs, Cameras


@admin.register(TrafficLogs)
class TrafficLogsAdmin(admin.ModelAdmin):
    list_display = ("plate_number", "camera_id", "timestamp", "type_id")
    list_filter = ("type_id",)
    search_fields = ("plate_number", "type_id")