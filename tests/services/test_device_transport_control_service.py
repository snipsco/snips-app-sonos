import pytest

from snipssonos.entities.device import Device
from snipssonos.services.device.transport_control import DeviceTransportControlService

@pytest.fixture
def connected_device():
    return Device.from_dict({
        'name': 'Antho',
        'identifier': 'RINCON_XXXXXX',
        'volume': 10
    })


def test_cant_use_transport_service_volume_up(connected_device):
    transport_service = DeviceTransportControlService()

    with pytest.raises(NotImplementedError):
        transport_service.volume_up(connected_device)


def test_cant_use_transport_service_volume_down(connected_device):
    transport_service = DeviceTransportControlService()

    with pytest.raises(NotImplementedError):
        transport_service.volume_down(connected_device)
