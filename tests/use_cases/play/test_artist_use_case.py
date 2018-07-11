import pytest
from mock import mock

from snipssonos.entities.device import Device
from snipssonos.entities.track import Track

from snipssonos.use_cases.play.artist import PlayArtistUseCase
from snipssonos.use_cases.request_objects import PlayArtistRequestFactory

from snipssonos.services.feedback.feedback_messages import FR_TTS_GENERIC_ERROR, FR_TTS_PLAYING_ARTIST_TEMPLATE

from snipssonos.exceptions import NoReachableDeviceException


@pytest.fixture
def connected_device():
    return Device(
        name="Anthony's Sonos",
        identifier="RINCON_XXXX",
        volume=10
    )


def test_use_case_empty_parameters():
    device_discovery_service = mock.Mock()
    music_search_service = mock.Mock()
    music_playback_service = mock.Mock()

    play_artist_uc = PlayArtistUseCase(device_discovery_service, music_search_service, music_playback_service)

    play_artist_request = PlayArtistRequestFactory.from_dict({})
    result_object = play_artist_uc.execute(play_artist_request)

    assert bool(play_artist_request) is False
    assert bool(result_object) is False


def test_use_case_no_reachable_device():
    device_discovery_service = mock.Mock()
    device_discovery_service.get.side_effect = NoReachableDeviceException(
        "No reachable Sonos devices")  # We mock the device discovery service

    device_transport_control_service = mock.Mock()
    music_playback_service = mock.Mock()

    play_artist_uc = PlayArtistUseCase(device_discovery_service, device_transport_control_service,
                                       music_playback_service)

    play_artist_request = PlayArtistRequestFactory.from_dict({'artist_name': 'Ibeyi'})
    result_obj = play_artist_uc.execute(play_artist_request)

    assert bool(result_obj) is False
    assert result_obj.message == "NoReachableDeviceException: No reachable Sonos devices"


def test_use_case_artist_success_tts():
    device_discovery_service = mock.Mock()
    music_search_service = mock.Mock()
    music_playback_service = mock.Mock()

    music_search_service.search_artist.return_value = [Track("", 'Deathless', 'Ibeyi')]
    play_artist_uc = PlayArtistUseCase(device_discovery_service, music_search_service,
                                       music_playback_service)

    play_artist_request = PlayArtistRequestFactory.from_dict({'artist_name': 'Ibeyi'})
    result_obj = play_artist_uc.execute(play_artist_request)

    assert bool(result_obj) is True
    assert result_obj.feedback == FR_TTS_PLAYING_ARTIST_TEMPLATE.format("Ibeyi")


def test_use_case_artist_failure_tts():
    device_discovery_service = mock.Mock()
    music_search_service = mock.Mock()
    music_playback_service = mock.Mock()

    music_search_service.search_artist.return_value = []
    play_artist_uc = PlayArtistUseCase(device_discovery_service, music_search_service,
                                       music_playback_service)

    play_artist_request = PlayArtistRequestFactory.from_dict({'artist_name': 'Ibeyi'})
    result_obj = play_artist_uc.execute(play_artist_request)

    assert bool(result_obj) is False
    assert result_obj.message == FR_TTS_GENERIC_ERROR

