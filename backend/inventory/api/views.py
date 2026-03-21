from rest_framework import viewsets

from backend.inventory.models import Equipment, MaintenanceLog

from .serializers import EquipmentSerializer, MaintenanceLogSerializer


class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer


class MaintenanceLogViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceLog.objects.all()
    serializer_class = MaintenanceLogSerializer

    def perform_create(self, serializer):
        # Automatically set the author to the logged-in user if available
        serializer.save(author=self.request.user if self.request.user.is_authenticated else None)
