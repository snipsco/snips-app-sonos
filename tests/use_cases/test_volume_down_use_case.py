import pytest
from mock import mock

from snipssonos.entities.device import Device
from snipssonos.use_cases.volume_down import VolumeDownUseCase
from snipssonos.use_cases.request_objects import VolumeDownRequestObject

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

    volume_down_uc = VolumeDownUseCase(device_discovery_service, device_transport_control_service)
    volume_down_request = VolumeDownRequestObject.from_dict({})
    result_object = volume_down_uc.execute(volume_down_request)

    device_discovery_service.get.assert_called()
    device_transport_control_service.volume_down.assert_called()

    device_transport_control_service.volume_down.assert_called_with(connected_device)

    assert bool(result_object) is True
    assert connected_device.volume == initial_volume - VolumeDownUseCase.DEFAULT_VOLUME_DECREMENT


def test_use_case_no_reachable_device():
    device_discovery_service = mock.Mock()
    device_discovery_service.get.side_effect = NoReachableDeviceException("No reachable Sonos devices")  # We mock the device discovery service

    device_transport_control_service = mock.Mock()

    volume_down_uc = VolumeDownUseCase(device_discovery_service, device_transport_control_service)

    volume_down_request = VolumeDownRequestObject()
    result_obj = volume_down_uc.execute(volume_down_request)

    assert bool(result_obj) is False
    assert result_obj.message == "NoReachableDeviceException: No reachable Sonos devices"


def test_use_case_with_wrong_parameter():
    volume_level_is_a_string = "duh"

    device_discovery_service = mock.Mock()
    device_discovery_service.get.return_value = connected_device  # We mock the device discovery service

    device_transport_control_service = mock.Mock()
    volume_down_uc = VolumeDownUseCase(device_discovery_service, device_transport_control_service)

    volume_down_request = VolumeDownRequestObject.from_dict({'volume_decrease' : volume_level_is_a_string})
    response_object = volume_down_uc.execute(volume_down_request)

    assert bool(response_object) is False


def test_use_case_with_parameter_out_of_range(connected_device):
    volume_increase_in_percentage = 123456789

    device_discovery_service = mock.Mock()
    device_discovery_service.get.return_value = connected_device  # We mock the device discovery service

    device_transport_control_service = mock.Mock()
    volume_down_uc = VolumeDownUseCase(device_discovery_service, device_transport_control_service)

    volume_down_request = VolumeDownRequestObject.from_dict({'volume_decrease': volume_increase_in_percentage})
    response_object = volume_down_uc.execute(volume_down_request)

    assert bool(response_object) is False
    assert connected_device.volume == 10


def test_use_case_with_positive_percentage(connected_device):
    volume_decrease_in_percentage = 10
    initial_volume = connected_device.volume

    device_discovery_service = mock.Mock()
    device_discovery_service.get.return_value = connected_device  # We mock the device discovery service

    device_transport_control_service = mock.Mock()
    volume_down_uc = VolumeDownUseCase(device_discovery_service, device_transport_control_service)

    volume_down_request = VolumeDownRequestObject.from_dict({'volume_decrease': volume_decrease_in_percentage})
    response_object = volume_down_uc.execute(volume_down_request)

    assert bool(response_object) is True
    device_transport_control_service.volume_down.assert_called_with(connected_device)
    assert connected_device.volume == initial_volume - volume_decrease_in_percentage


def test_use_case_with_negative_percentage(connected_device):
    volume_decrease_in_percentage = -10

    device_discovery_service = mock.Mock()
    device_discovery_service.get.return_value = connected_device  # We mock the device discovery service

    device_transport_control_service = mock.Mock()
    volume_down_uc = VolumeDownUseCase(device_discovery_service, device_transport_control_service)

    volume_down_request = VolumeDownRequestObject.from_dict({'volume_decrease': volume_decrease_in_percentage})
    response_object = volume_down_uc.execute(volume_down_request)

    assert bool(response_object) is False
    assert connected_device.volume == 10


def test_use_case_with_positive_integer(connected_device):
    volume_decrease_integer = 10
    initial_volume = connected_device.volume

    device_discovery_service = mock.Mock()
    device_discovery_service.get.return_value = connected_device  # We mock the device discovery service

    device_transport_control_service = mock.Mock()
    volume_down_uc = VolumeDownUseCase(device_discovery_service, device_transport_control_service)

    volume_down_request = VolumeDownRequestObject.from_dict({'volume_decrease' : volume_decrease_integer})
    response_object = volume_down_uc.execute(volume_down_request)

    assert bool(response_object) is True
    device_transport_control_service.volume_down.assert_called_with(connected_device)
    assert connected_device.volume == initial_volume - volume_decrease_integer


def test_use_case_with_negative_integer(connected_device):
    volume_decrease_integer = -10

    device_discovery_service = mock.Mock()
    device_discovery_service.get.return_value = connected_device  # We mock the device discovery service

    device_transport_control_service = mock.Mock()
    volume_down_uc = VolumeDownUseCase(device_discovery_service, device_transport_control_service)

    volume_down_request = VolumeDownRequestObject.from_dict({'volume_decrease': volume_decrease_integer})
    response_object = volume_down_uc.execute(volume_down_request)

    assert bool(response_object) is False
    assert connected_device.volume == 10


def test_use_case_with_maximum_volume(connected_device):
    volume_decrease_integer = 11

    device_discovery_service = mock.Mock()
    device_discovery_service.get.return_value = connected_device  # We mock the device discovery service

    device_transport_control_service = mock.Mock()
    volume_down_uc = VolumeDownUseCase(device_discovery_service, device_transport_control_service)

    volume_down_request = VolumeDownRequestObject.from_dict({'volume_decrease': volume_decrease_integer})
    response_object = volume_down_uc.execute(volume_down_request)

    assert bool(response_object) is True
    assert connected_device.volume == 0


