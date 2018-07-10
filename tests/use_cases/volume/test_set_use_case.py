import pytest
from mock import mock

from snipssonos.entities.device import Device
from snipssonos.use_cases.volume.set import VolumeSetUseCase
from snipssonos.use_cases.request_objects import VolumeSetRequestObject, VolumeSetRequestFactory

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
    device_discovery_service.get_devices.return_value = [connected_device]  # We mock the device discovery service

    initial_volume = connected_device.volume

    device_transport_control_service = mock.Mock()

    volume_set_uc = VolumeSetUseCase(device_discovery_service, device_transport_control_service)
    volume_set_request = VolumeSetRequestFactory.from_dict({})
    result_object = volume_set_uc.execute(volume_set_request)

    device_discovery_service.get.assert_not_called()
    device_transport_control_service.volume_set.assert_not_called()
    assert bool(volume_set_request) is False
    assert bool(result_object) is False
    assert connected_device.volume == initial_volume


def test_use_case_no_reachable_device():
    device_discovery_service = mock.Mock()
    device_discovery_service.get_devices.side_effect = NoReachableDeviceException(
        "No reachable Sonos devices")  # We mock the device discovery service

    device_transport_control_service = mock.Mock()

    volume_set_uc = VolumeSetUseCase(device_discovery_service, device_transport_control_service)

    volume_set_request = VolumeSetRequestFactory.from_dict({'volume_level': 10})
    result_obj = volume_set_uc.execute(volume_set_request)

    assert bool(result_obj) is False
    assert result_obj.message == "NoReachableDeviceException: No reachable Sonos devices"


def test_use_case_with_wrong_parameter():
    volume_level_is_a_string = "duh"

    device_discovery_service = mock.Mock()
    device_discovery_service.get_devices.return_value = [connected_device]  # We mock the device discovery service

    device_transport_control_service = mock.Mock()
    volume_set_uc = VolumeSetUseCase(device_discovery_service, device_transport_control_service)

    volume_set_request = VolumeSetRequestFactory.from_dict({'volume_level': volume_level_is_a_string})
    response_object = volume_set_uc.execute(volume_set_request)

    assert bool(response_object) is False


def test_use_case_with_parameter_out_of_range(connected_device):
    volume_increase_in_percentage = 123456789

    device_discovery_service = mock.Mock()
    device_discovery_service.get_devices.return_value = [connected_device]  # We mock the device discovery service

    device_transport_control_service = mock.Mock()
    volume_set_uc = VolumeSetUseCase(device_discovery_service, device_transport_control_service)

    volume_set_request = VolumeSetRequestFactory.from_dict({'volume_level': volume_increase_in_percentage})
    response_object = volume_set_uc.execute(volume_set_request)

    assert bool(response_object) is False
    assert connected_device.volume == 10


def test_use_case_with_positive_percentage(connected_device):
    new_volume_level = 50
    initial_volume = connected_device.volume

    device_discovery_service = mock.Mock()
    device_discovery_service.get_devices.return_value = [connected_device]  # We mock the device discovery service

    device_transport_control_service = mock.Mock()
    volume_set_uc = VolumeSetUseCase(device_discovery_service, device_transport_control_service)

    volume_set_request = VolumeSetRequestFactory.from_dict({'volume_level': new_volume_level})
    response_object = volume_set_uc.execute(volume_set_request)

    assert bool(volume_set_request) is True
    assert bool(response_object) is True
    device_transport_control_service.set_volume.assert_called_with(connected_device)
    assert connected_device.volume == new_volume_level


def test_use_case_with_negative_percentage(connected_device):
    volume_negative_level = -10

    device_discovery_service = mock.Mock()
    device_discovery_service.get_devices.return_value = [connected_device]  # We mock the device discovery service

    device_transport_control_service = mock.Mock()
    volume_set_uc = VolumeSetUseCase(device_discovery_service, device_transport_control_service)

    volume_set_request = VolumeSetRequestFactory.from_dict({'volume_level': volume_negative_level})
    response_object = volume_set_uc.execute(volume_set_request)

    assert bool(response_object) is False
    assert connected_device.volume == 10


def test_use_case_with_positive_integer(connected_device):
    volume_level = 40
    initial_volume = connected_device.volume

    device_discovery_service = mock.Mock()
    device_discovery_service.get_devices.return_value = [connected_device]  # We mock the device discovery service
    device_transport_control_service = mock.Mock()

    volume_set_uc = VolumeSetUseCase(device_discovery_service, device_transport_control_service)

    volume_set_request = VolumeSetRequestFactory.from_dict({'volume_level': volume_level})
    response_object = volume_set_uc.execute(volume_set_request)

    assert bool(volume_set_request) is True
    assert bool(response_object) is True
    device_transport_control_service.set_volume.assert_called_with(connected_device)
    assert connected_device.volume == volume_level


def test_use_case_with_negative_integer(connected_device):
    volume_level_negative = -10

    device_discovery_service = mock.Mock()
    device_discovery_service.get_devices.return_value = [connected_device]  # We mock the device discovery service

    device_transport_control_service = mock.Mock()
    volume_set_uc = VolumeSetUseCase(device_discovery_service, device_transport_control_service)

    volume_set_request = VolumeSetRequestFactory.from_dict({'volume_level': volume_level_negative})
    response_object = volume_set_uc.execute(volume_set_request)

    assert bool(response_object) is False
    assert connected_device.volume == 10


def test_use_case_with_maximum_volume(connected_device):
    volume_level = 100

    device_discovery_service = mock.Mock()
    device_discovery_service.get_devices.return_value = [connected_device]  # We mock the device discovery service

    device_transport_control_service = mock.Mock()
    volume_set_uc = VolumeSetUseCase(device_discovery_service, device_transport_control_service)

    volume_set_request = VolumeSetRequestFactory.from_dict({'volume_level': volume_level})
    response_object = volume_set_uc.execute(volume_set_request)

    assert bool(response_object) is True
    assert connected_device.volume == 100
