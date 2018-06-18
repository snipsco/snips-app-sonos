import pytest
from mock import mock

from snipssonos.entities.device import Device
from snipssonos.use_cases.mute import MuteUseCase
from snipssonos.use_cases.request_objects import MuteRequestFactory

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

    initial_volume = connected_device.volume

    device_transport_control_service = mock.Mock()

    mute_uc = MuteUseCase(device_discovery_service, device_transport_control_service)
    mute_request_object = MuteRequestFactory.from_dict({})
    result_object = mute_uc.execute(mute_request_object)

    device_discovery_service.get.assert_called()
    device_transport_control_service.mute.assert_called()

    device_transport_control_service.mute.assert_called_with(connected_device)

    assert bool(result_object) is True
    assert connected_device.volume == initial_volume


def test_use_case_no_reachable_device():
    device_discovery_service = mock.Mock()
    device_discovery_service.get.side_effect = NoReachableDeviceException(
        "No reachable Sonos devices")  # We mock the device discovery service

    device_transport_control_service = mock.Mock()

    mute_uc = MuteUseCase(device_discovery_service, device_transport_control_service)

    mute_request = MuteRequestFactory.from_dict({})
    result_obj = mute_uc.execute(mute_request)

    assert bool(result_obj) is False
    assert result_obj.message == "NoReachableDeviceException: No reachable Sonos devices"
