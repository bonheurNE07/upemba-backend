from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from backend.inventory.api.views import EquipmentViewSet, MaintenanceLogViewSet
from backend.telemetry.api.views import HealthStatusViewSet, SensorReadingViewSet
from backend.users.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("equipment", EquipmentViewSet)
router.register("maintenance-logs", MaintenanceLogViewSet)
router.register("health-status", HealthStatusViewSet)
router.register("sensor-readings", SensorReadingViewSet)


app_name = "api"
urlpatterns = router.urls
