import mock
import pytest
import requests

from snipssonos.services.node.device_transport_control import NodeDeviceTransportControlService
from snipssonos.exceptions import NoReachableDeviceException
from snipssonos.use_cases.volume.up import VolumeUpUseCase
from snipssonos.entities.device import Device


@pytest.fixture
def connected_device():
    return Device.from_dict(
        {
            'identifier': 'RINCON_XXXX',
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

    assert transport_service._generate_volume_query(room_name, volume_level) == "http://localhost:5005/Antho/volume/10"


def test_generate_url_query_for_resume(connected_device):
    PROTOCOL = NodeDeviceTransportControlService.PROTOCOL
    HOST = NodeDeviceTransportControlService.HOST
    PORT = NodeDeviceTransportControlService.PORT

    room_name = connected_device.name
    volume_level = 10

    transport_service = NodeDeviceTransportControlService()

    assert transport_service._generate_resume_query(room_name) == "http://localhost:5005/Antho/play"


def test_generate_url_query_for_mute(connected_device):
    PROTOCOL = NodeDeviceTransportControlService.PROTOCOL
    HOST = NodeDeviceTransportControlService.HOST
    PORT = NodeDeviceTransportControlService.PORT

    room_name = connected_device.name
    volume_level = 10

    transport_service = NodeDeviceTransportControlService()

    assert transport_service._generate_mute_query(room_name) == "http://localhost:5005/Antho/mute"


def test_generate_url_query_for_next_track(connected_device):
    PROTOCOL = NodeDeviceTransportControlService.PROTOCOL
    HOST = NodeDeviceTransportControlService.HOST
    PORT = NodeDeviceTransportControlService.PORT

    room_name = connected_device.name
    volume_level = 10

    transport_service = NodeDeviceTransportControlService()

    assert transport_service._generate_next_track_query(room_name) == "http://localhost:5005/Antho/next"


@mock.patch('snipssonos.services.node.device_transport_control.requests')
def test_volume_up_method_performs_correct_api_query(mocked_requests, connected_device):
    transport_service = NodeDeviceTransportControlService()
    volume_increment = VolumeUpUseCase.DEFAULT_VOLUME_INCREMENT

    connected_device.increase_volume(volume_increment)
    transport_service.volume_up(connected_device)

    mocked_requests.get.assert_called_with(
        transport_service._generate_volume_query(connected_device.name, connected_device.volume))


@mock.patch('snipssonos.services.node.device_transport_control.requests')
def test_volume_up_method_failure_raises_exception(mocked_requests, connected_device):
    transport_service = NodeDeviceTransportControlService()
    volume_increment = VolumeUpUseCase.DEFAULT_VOLUME_INCREMENT

    connected_device.increase_volume(volume_increment)
    mocked_response_object = mock.create_autospec(requests.Response)
    mocked_response_object.ok = False

    mocked_requests.get.return_value = mocked_response_object

    with pytest.raises(NoReachableDeviceException):
        transport_service.volume_up(connected_device)


@mock.patch('snipssonos.services.node.device_transport_control.requests')
def test_mute_method_performs_correct_api_query(mocked_requests, connected_device):
    transport_service = NodeDeviceTransportControlService()

    transport_service.mute(connected_device)

    mocked_requests.get.assert_called_with(
        transport_service._generate_mute_query(connected_device.name))


@mock.patch('snipssonos.services.node.device_transport_control.requests')
def test_volume_up_method_failure_raises_exception(mocked_requests, connected_device):
    transport_service = NodeDeviceTransportControlService()

    mocked_response_object = mock.create_autospec(requests.Response)
    mocked_response_object.ok = False

    mocked_requests.get.return_value = mocked_response_object

    with pytest.raises(NoReachableDeviceException):
        transport_service.mute(connected_device)
