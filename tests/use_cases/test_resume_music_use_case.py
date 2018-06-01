import pytest
from mock import mock

from snipssonos.entities.device import Device
from snipssonos.use_cases.resume_music import ResumeMusicUseCase
from snipssonos.use_cases.request_objects import ResumeMusicRequestObject

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

    resume_music_uc = ResumeMusicUseCase(device_discovery_service, device_transport_control_service)
    resume_music_request = ResumeMusicRequestObject.from_dict({})
    result_object = resume_music_uc.execute(resume_music_request)

    device_discovery_service.get.assert_called()
    device_transport_control_service.resume.assert_called()

    assert bool(result_object) is True


def test_use_case_no_reachable_device():
    device_discovery_service = mock.Mock()
    device_discovery_service.get.side_effect = NoReachableDeviceException("No reachable Sonos devices")  # We mock the device discovery service

    device_transport_control_service = mock.Mock()

    resume_music_uc = ResumeMusicUseCase(device_discovery_service, device_transport_control_service)

    resume_music_request = ResumeMusicRequestObject()
    result_obj = resume_music_uc.execute(resume_music_request)

    assert bool(result_obj) is False
    assert result_obj.message == "NoReachableDeviceException: No reachable Sonos devices"
