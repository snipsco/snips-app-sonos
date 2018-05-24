import mock
import pytest
import requests

from snipssonos.services.node_device_transport_control import NodeDeviceTransportControlService
from snipssonos.exceptions import NoReachableDeviceException
from snipssonos.use_cases.volume_up import VolumeUpUseCase
from snipssonos.entities.device import Device

@pytest.fixture
def connected_device():
    return Device.from_dict(
        {
            'identifier':'RINCON_XXXX',
            'name': 'Antho',
            'volume': 10
        }
    )


def test_transport_control_service_initialization():
    transport_service = NodeDeviceTransportControlService()

    assert transport_service.PORT == NodeDeviceTransportControlService.PORT
    assert transport_service.HOST == NodeDeviceTransportControlService.HOST
    assert transport_service.PROTOCOL == NodeDeviceTransportControlService.PROTOCOL


def test_generate_url_query_for_volume_up(connected_device):
    PROTOCOL = NodeDeviceTransportControlService.PROTOCOL
    HOST = NodeDeviceTransportControlService.HOST
    PORT = NodeDeviceTransportControlService.PORT

    room_name = connected_device.name
    volume_level = 10

    transport_service = NodeDeviceTransportControlService()

    assert transport_service.generate_volume_up_query(room_name, volume_level) == "http://localhost:5005/Antho/volume/10"


@mock.patch('snipssonos.services.node_device_transport_control.requests')
def test_volume_up_method_performs_correct_api_query(mocked_requests, connected_device):
    transport_service = NodeDeviceTransportControlService()
    volume_increment = VolumeUpUseCase.DEFAULT_VOLUME_INCREMENT

    transport_service.volume_up(connected_device, volume_increment)

    mocked_requests.get.assert_called_with(
        transport_service.generate_volume_up_query(connected_device.name, connected_device.volume + volume_increment))

@mock.patch('snipssonos.services.node_device_transport_control.requests')
def test_volume_up_method_failure_raises_exception(mocked_requests, connected_device):
    transport_service = NodeDeviceTransportControlService()
    volume_increment = VolumeUpUseCase.DEFAULT_VOLUME_INCREMENT

    mocked_response_object = mock.create_autospec(requests.Response)
    mocked_response_object.ok = False

    mocked_requests.get.return_value = mocked_response_object

    with pytest.raises(NoReachableDeviceException):
        transport_service.volume_up(connected_device, volume_increment)
