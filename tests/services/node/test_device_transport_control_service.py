import pytest
import requests
from mock import mock, patch

from snipssonos.services.node.device_transport_control import NodeDeviceTransportControlService
from snipssonos.exceptions import NoReachableDeviceException
from snipssonos.use_cases.volume.up import VolumeUpUseCase
from snipssonos.entities.device import Device


@pytest.fixture
def node_configuration():
    return {
        'global' : {
            'node_device_transport_control_port' : 5005 ,
            'node_device_transport_control_host' : 'localhost'
        }
    }

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


def test_generate_url_query_for_volume_up(connected_device, node_configuration):
    PROTOCOL = NodeDeviceTransportControlService.PROTOCOL
    HOST = NodeDeviceTransportControlService.HOST
    PORT = NodeDeviceTransportControlService.PORT

    room_name = connected_device.name
    volume_level = 10

    transport_service = NodeDeviceTransportControlService(node_configuration)

    assert transport_service._generate_volume_query(room_name, volume_level) == "http://localhost:5005/Antho/volume/10"


def test_generate_url_query_for_resume(connected_device, node_configuration):
    PROTOCOL = NodeDeviceTransportControlService.PROTOCOL
    HOST = NodeDeviceTransportControlService.HOST
    PORT = NodeDeviceTransportControlService.PORT

    room_name = connected_device.name
    volume_level = 10

    transport_service = NodeDeviceTransportControlService(node_configuration)

    assert transport_service._generate_resume_query(room_name) == "http://localhost:5005/Antho/play"


def test_generate_url_query_for_mute(connected_device, node_configuration):
    PROTOCOL = NodeDeviceTransportControlService.PROTOCOL
    HOST = NodeDeviceTransportControlService.HOST
    PORT = NodeDeviceTransportControlService.PORT

    room_name = connected_device.name
    volume_level = 10

    transport_service = NodeDeviceTransportControlService(node_configuration)

    assert transport_service._generate_mute_query(room_name) == "http://localhost:5005/Antho/mute"


def test_generate_url_query_for_next_track(connected_device, node_configuration):
    PROTOCOL = NodeDeviceTransportControlService.PROTOCOL
    HOST = NodeDeviceTransportControlService.HOST
    PORT = NodeDeviceTransportControlService.PORT

    room_name = connected_device.name
    volume_level = 10

    transport_service = NodeDeviceTransportControlService(node_configuration)

    assert transport_service._generate_next_track_query(room_name) == "http://localhost:5005/Antho/next"


def test_generate_url_query_for_previous_track(connected_device):
    protocol = NodeDeviceTransportControlService.PROTOCOL
    host = NodeDeviceTransportControlService.HOST
    port = NodeDeviceTransportControlService.PORT

    room_name = connected_device.name
    expected_query = "{}{}:{}/{}/previous".format(protocol, host, port, room_name)

    transport_service = NodeDeviceTransportControlService()
    assert transport_service._generate_previous_track_query(room_name) == expected_query


def test_generate_url_query_for_state(connected_device):
    protocol = NodeDeviceTransportControlService.PROTOCOL
    host = NodeDeviceTransportControlService.HOST
    port = NodeDeviceTransportControlService.PORT

    room_name = connected_device.name
    expected_query = "{}{}:{}/{}/trackseek/1".format(protocol, host, port, room_name)

    transport_service = NodeDeviceTransportControlService()
    assert transport_service._generate_track_seek_query(room_name, 1) == expected_query


def test_generate_url_query_for_track_seek_query(connected_device):
    protocol = NodeDeviceTransportControlService.PROTOCOL
    host = NodeDeviceTransportControlService.HOST
    port = NodeDeviceTransportControlService.PORT

    room_name = connected_device.name
    expected_query = "{}{}:{}/{}/state".format(protocol, host, port, room_name)

    transport_service = NodeDeviceTransportControlService()
    assert transport_service._generate_state_query(room_name) == expected_query


@mock.patch('snipssonos.services.node.device_transport_control.requests.Response')
def test_extract_state_track_number(mock_response):
    mock_response.json.return_value = {
        'trackNo': 1
    }

    transport_service = NodeDeviceTransportControlService()
    assert transport_service._extract_state_track_number(mock_response) == 1


@mock.patch('snipssonos.services.node.device_transport_control.requests')
def test_get_track_number(mock_request, connected_device):
    mocked_response = mock.create_autospec(requests.Response)
    mocked_response.ok = True

    mocked_response.json.return_value = {
        'trackNo': 1
    }
    mock_request.get.return_value = mocked_response

    transport_service = NodeDeviceTransportControlService()
    assert transport_service.get_track_number(connected_device.name) == 1


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


@mock.patch('snipssonos.services.node.device_transport_control.requests')
@patch.object(NodeDeviceTransportControlService, 'get_track_number')
def test_transport_service_previous_track_correct_api_query_for_not_first_track_in_queue(mock_get_track_number,
                                                                                         mock_request, connected_device):
    mocked_response_object = mock.create_autospec(requests.Response)
    mocked_response_object.ok = True

    mock_request.get.return_value = mocked_response_object

    mock_get_track_number.return_value = 3
    transport_service = NodeDeviceTransportControlService()

    transport_service.previous_track(connected_device)
    mock_request.get.assert_called_with(
        transport_service._generate_previous_track_query(connected_device.name))


@mock.patch('snipssonos.services.node.device_transport_control.requests')
@patch.object(NodeDeviceTransportControlService, 'get_track_number')
def test_transport_service_previous_track_correct_api_query_for_first_track_in_queue(mock_get_track_number,
                                                                                         mock_request, connected_device):
    mocked_response_object = mock.create_autospec(requests.Response)
    mocked_response_object.ok = True

    mock_request.get.return_value = mocked_response_object

    mock_get_track_number.return_value = 1
    transport_service = NodeDeviceTransportControlService()

    transport_service.previous_track(connected_device)
    mock_request.get.assert_called_with(
        transport_service._generate_track_seek_query(connected_device.name, 1))


@mock.patch('snipssonos.services.node.device_transport_control.requests')
def test_transport_service_get_info_does_correct_api_query(mock_request, connected_device):
    mocked_response_object = mock.create_autospec(requests.Response)
    mocked_response_object.ok = True
    mocked_response_object.json.return_value = {
        'currentTrack': {
            'title': 'Teenage Fantasy',
            'artist': 'Jorja Smith'
        }
    }

    mock_request.get.return_value = mocked_response_object
    transport_service = NodeDeviceTransportControlService()

    transport_service.get_track_info(connected_device)

    mock_request.get.assert_called_with(
        transport_service._generate_state_query(connected_device.name))


@mock.patch('snipssonos.services.node.device_transport_control.requests')
def test_transport_service_get_info_return_title_and_artist(mock_request, connected_device):
    mocked_response_object = mock.create_autospec(requests.Response)
    mocked_response_object.ok = True
    mocked_response_object.json.return_value = {
        'currentTrack': {
            'title': 'Teenage Fantasy',
            'artist': 'Jorja Smith'
        }
    }

    mock_request.get.return_value = mocked_response_object
    transport_service = NodeDeviceTransportControlService()

    transport_service.get_track_info(connected_device)
    title, artist = transport_service.get_track_info(connected_device)
    print(title, artist)

    assert title == "Teenage Fantasy"
    assert artist == "Jorja Smith"

