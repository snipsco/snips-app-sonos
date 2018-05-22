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


def test_use_case_with_wrong_parameter():
    volume_level_is_a_string = "duh"

    device_discovery_service = mock.Mock()
    device_discovery_service.get.return_value = connected_device  # We mock the device discovery service

    device_transport_control_service = mock.Mock()
    volume_up_uc = VolumeUpUseCase(device_discovery_service, device_transport_control_service)

    volume_up_request = VolumeUpRequestObject.from_dict({"volume": volume_level_is_a_string})
    response_object = volume_up_uc.execute(volume_up_request)

    assert bool(response_object) is True


def test_use_case_with_parameter_out_of_range():
    assert True is False


def test_use_case_with_positive_percentage(connected_device):
    volume_level_in_percentage = 10

    device_discovery_service = mock.Mock()
    device_discovery_service.get.return_value = connected_device  # We mock the device discovery service

    device_transport_control_service = mock.Mock()
    volume_up_uc = VolumeUpUseCase(device_discovery_service, device_transport_control_service)

    volume_up_request = VolumeUpRequestObject.from_dict({"volume_increase_in_percent" : volume_level_in_percentage})
    response_object = volume_up_uc.execute(volume_up_request)

    assert bool(response_object) is True
    device_transport_control_service.volume_up.assert_called_with(connected_device, volume_level_in_percentage)
    # We assert that the device now has an increased volume of 10%



def test_use_case_with_negative_percentage():
    assert True is False


def test_use_case_with_positive_integer():
    assert True is False


def test_use_case_with_negative_integer():
    assert True is False


def test_use_case_with_maximum_volume():
    assert True is False


