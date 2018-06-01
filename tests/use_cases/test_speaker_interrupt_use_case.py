import pytest
from mock import mock

from snipssonos.entities.device import Device
from snipssonos.use_cases.speaker_interrupt import SpeakerInterruptUseCase
from snipssonos.use_cases.request_objects import SpeakerInterruptRequestObject

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

    speaker_interrupt_uc = SpeakerInterruptUseCase(device_discovery_service, device_transport_control_service)
    speaker_interrupt_request = SpeakerInterruptRequestObject.from_dict({})
    result_object = speaker_interrupt_uc.execute(speaker_interrupt_request)

    device_discovery_service.get.assert_called()
    device_transport_control_service.pause.assert_called()

    device_transport_control_service.pause.assert_called_with(connected_device)

    assert bool(result_object) is True



def test_use_case_no_reachable_device():
    device_discovery_service = mock.Mock()
    device_discovery_service.get.side_effect = NoReachableDeviceException("No reachable Sonos devices")  # We mock the device discovery service

    device_transport_control_service = mock.Mock()

    speaker_interrupt_uc = SpeakerInterruptUseCase(device_discovery_service, device_transport_control_service)

    speaker_interrupt_request = SpeakerInterruptRequestObject()
    result_obj = speaker_interrupt_uc.execute(speaker_interrupt_request)

    assert bool(result_obj) is False
    assert result_obj.message == "NoReachableDeviceException: No reachable Sonos devices"
