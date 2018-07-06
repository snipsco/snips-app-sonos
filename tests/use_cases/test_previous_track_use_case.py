import pytest
from mock import mock

from snipssonos.entities.device import Device
from snipssonos.use_cases.previous_track import PreviousTrackUseCase
from snipssonos.use_cases.request_objects import PreviousTrackRequestFactory

from snipssonos.exceptions import NoReachableDeviceException


@pytest.fixture
def connected_device():
    return Device(
        name="Anthony's Sonos",
        identifier="RINCON_XXXX",
        volume=10
    )


def test_use_case_empty_parameters(connected_device):
    device_discovery_service = mock.Mock()
    device_discovery_service.get.return_value = connected_device  # We mock the device discovery service

    device_transport_control_service = mock.Mock()

    previous_track_uc = PreviousTrackUseCase(device_discovery_service, device_transport_control_service)
    previous_track_request = PreviousTrackRequestFactory.from_dict({})
    result_object = previous_track_uc.execute(previous_track_request)

    device_discovery_service.get.assert_called()
    device_transport_control_service.previous_track.assert_called()

    assert bool(result_object) is True


def test_use_case_no_reachable_device():
    device_discovery_service = mock.Mock()
    device_discovery_service.get.side_effect = NoReachableDeviceException(
        "No reachable Sonos devices")  # We mock the device discovery service

    device_transport_control_service = mock.Mock()

    previous_track_uc = PreviousTrackUseCase(device_discovery_service, device_transport_control_service)

    previous_track_request = PreviousTrackRequestFactory.from_dict({})
    result_obj = previous_track_uc.execute(previous_track_request)

    assert bool(result_obj) is False
    assert result_obj.message == "NoReachableDeviceException: No reachable Sonos devices"
