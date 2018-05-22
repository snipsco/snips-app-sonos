import pytest
from mock import mock

from snipssonos.entities.device import Device
from snipssonos.use_cases.volume_up import VolumeUpUseCase
from snipssonos.use_cases.request_objects import VolumeUpRequestObject

from snipssonos.exceptions import NoReachableDeviceException

@pytest.fixture
def connected_device():
    return Device(
        name="Anthony's Sonos",
        identifier="RINCON_XXXX"
    )

def test_use_case_empty_parameters():
    device_discovery_service = mock.Mock()
    device_discovery_service.get.return_value = connected_device  # We mock the device discovery service

    device_transport_control_service = mock.Mock()

    volume_up_uc = VolumeUpUseCase(device_discovery_service, device_transport_control_service)
    volume_up_request = VolumeUpRequestObject.from_dict({})
    result_object = volume_up_uc.execute(volume_up_request)

    device_discovery_service.get.assert_called()
    device_transport_control_service.volume_up.assert_called()

    assert bool(result_object) is True

def test_use_case_no_reachable_device():
    device_discovery_service = mock.Mock()
    device_discovery_service.get.side_effect = NoReachableDeviceException("No reachable Sonos devices")  # We mock the device discovery service

    device_transport_control_service = mock.Mock()

    volume_up_uc = VolumeUpUseCase(device_discovery_service, device_transport_control_service)

    volume_up_request = VolumeUpRequestObject()
    result_obj = volume_up_uc.execute(volume_up_request)

    assert bool(result_obj) is False
    assert result_obj.message == "NoReachableDeviceException: No reachable Sonos devices"

