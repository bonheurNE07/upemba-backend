import pytest

from backend.users.models import User
from backend.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def _media_storage(settings, tmpdir) -> None:
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user(db) -> User:
    return UserFactory.create()


@pytest.fixture
def equipment(db):
    from backend.inventory.tests.factories import EquipmentFactory
    return EquipmentFactory.create()


@pytest.fixture
def maintenance_log(db):
    from backend.inventory.tests.factories import MaintenanceLogFactory
    return MaintenanceLogFactory.create()


@pytest.fixture
def sensor_reading(db):
    from backend.telemetry.tests.factories import SensorReadingFactory
    return SensorReadingFactory.create()


@pytest.fixture
def health_status(db):
    from backend.telemetry.tests.factories import HealthStatusFactory
    return HealthStatusFactory.create()
