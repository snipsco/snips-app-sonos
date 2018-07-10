import pytest
from mock import mock

from snipssonos.entities.device import Device
from snipssonos.entities.track import Track
from snipssonos.entities.artist import Artist

from snipssonos.use_cases.get_track_info import GetTrackInfoUseCase
from snipssonos.use_cases.request_objects import GetTrackInfoRequestFactory

from snipssonos.shared.feedback import FR_TTS_TRACK_INFO_NO_TRACKS_ERROR


@pytest.fixture
def connected_device():
    return Device(
        name="Anthony's Sonos",
        identifier="RINCON_XXXX",
        volume=10
    )


def test_get_track_info_use_case_success_tts(connected_device):
    device_discovery_service = mock.Mock()
    device_discovery_service.get.return_value = connected_device  # We mock the device discovery service

    device_transport_control_service = mock.Mock()
    device_transport_control_service.get_track_info.return_value = Track("", "Away Away"), Artist("", "Ibeyi")

    get_track_info_uc = GetTrackInfoUseCase(device_discovery_service, device_transport_control_service)
    get_track_info_request = GetTrackInfoRequestFactory.from_dict({})
    result_object = get_track_info_uc.execute(get_track_info_request)

    device_discovery_service.get.assert_called()
    device_transport_control_service.get_track_info.assert_called()

    assert bool(result_object) is True
    assert result_object.feedback == "C'est Away Away par Ibeyi"


def test_get_track_info_use_case_failure_tts(connected_device):
    device_discovery_service = mock.Mock()
    device_discovery_service.get.return_value = connected_device  # We mock the device discovery service

    device_transport_control_service = mock.Mock()
    device_transport_control_service.get_track_info.return_value = Track("", ""), Artist("", "")

    get_track_info_uc = GetTrackInfoUseCase(device_discovery_service, device_transport_control_service)
    get_track_info_request = GetTrackInfoRequestFactory.from_dict({})
    result_object = get_track_info_uc.execute(get_track_info_request)

    device_discovery_service.get.assert_called()
    device_transport_control_service.get_track_info.assert_called()

    assert bool(result_object) is False
    assert result_object.message == FR_TTS_TRACK_INFO_NO_TRACKS_ERROR
