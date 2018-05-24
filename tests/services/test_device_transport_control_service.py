import pytest

from snipssonos.entities.device import Device
from snipssonos.services.device_transport_control import DeviceTransportControlService
from snipssonos.use_cases.volume_up import VolumeUpUseCase



@pytest.fixture
def connected_device():
    return Device.from_dict({
        'name':'Antho',
        'identifier': 'RINCON_XXXXXX',
        'volume':10
    })

def test_cant_use_transport_service_volume_up(connected_device):
    transport_service = DeviceTransportControlService()
    increment = 10

    with pytest.raises(NotImplementedError):
        transport_service.volume_up(connected_device, increment)




