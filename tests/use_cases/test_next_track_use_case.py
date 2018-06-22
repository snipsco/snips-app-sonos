import pytest
from mock import mock

from snipssonos.entities.device import Device
from snipssonos.use_cases.next_track import NextTrackUseCase
from snipssonos.use_cases.request_objects import NextTrackRequestObject, NextTrackRequestFactory

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

    next_track_uc = NextTrackUseCase(device_discovery_service, device_transport_control_service)
    next_track_request = NextTrackRequestFactory.from_dict({})
    result_object = next_track_uc.execute(next_track_request)

    device_discovery_service.get.assert_called()
    device_transport_control_service.next_track.assert_called()

    assert bool(result_object) is True


def test_use_case_no_reachable_device():
    device_discovery_service = mock.Mock()
    device_discovery_service.get.side_effect = NoReachableDeviceException(
        "No reachable Sonos devices")  # We mock the device discovery service

    device_transport_control_service = mock.Mock()

    next_track_uc = NextTrackUseCase(device_discovery_service, device_transport_control_service)

    next_track_request = NextTrackRequestFactory.from_dict({})
    result_obj = next_track_uc.execute(next_track_request)

    assert bool(result_obj) is False
    assert result_obj.message == "NoReachableDeviceException: No reachable Sonos devices"

