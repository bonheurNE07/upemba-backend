from django.contrib import admin
from .models import SensorReading, HealthStatus

@admin.register(SensorReading)
class SensorReadingAdmin(admin.ModelAdmin):
    list_display = ["equipment", "timestamp", "temperature", "voltage", "current", "vibration_x"]
    list_filter = ["equipment", "timestamp"]
    search_fields = ["equipment__name", "equipment__mac_address"]
    readonly_fields = ["timestamp"]

@admin.register(HealthStatus)
class HealthStatusAdmin(admin.ModelAdmin):
    list_display = ["equipment", "timestamp", "status", "anomaly_score"]
    list_filter = ["status", "equipment"]
    search_fields = ["equipment__name"]
    readonly_fields = ["timestamp"]
