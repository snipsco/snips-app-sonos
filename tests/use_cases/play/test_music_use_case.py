import pytest
from mock import mock

from snipssonos.entities.device import Device

from snipssonos.use_cases.play.music import PlayMusicUseCase
from snipssonos.use_cases.request_objects import PlayMusicRequestFactory

from snipssonos.exceptions import NoReachableDeviceException


@pytest.fixture
def connected_device():
    return Device(
        name="Anthony's Sonos",
        identifier="RINCON_XXXX",
        volume=10
    )


def test_use_case_empty_parameters(connected_device):
    device_disco_service = mock.Mock()
    music_playback_service = mock.Mock()
    music_search_service = mock.Mock()
    feedback_service = mock.Mock()

    play_artist_uc = PlayMusicUseCase(device_disco_service, music_search_service,
                                      music_playback_service, feedback_service)

    play_artist_request = PlayMusicRequestFactory.from_dict({})

    result_object = play_artist_uc.execute(play_artist_request)

    assert bool(result_object) is False
    device_disco_service.get.assert_not_called()


def test_use_case_no_reachable_device():
    device_discovery_service = mock.Mock()
    device_discovery_service.get.side_effect = NoReachableDeviceException(
        "No reachable Sonos devices")  # We mock the device discovery service

    music_search_service = mock.Mock()
    music_playback_service = mock.Mock()
    feedback_service = mock.Mock()

    playmusic_up_uc = PlayMusicUseCase(device_discovery_service, music_search_service,
                                       music_playback_service, feedback_service)

    playmusic_request = PlayMusicRequestFactory.from_dict({'artist_name': 'Antho'})
    result_obj = playmusic_up_uc.execute(playmusic_request)

    assert bool(result_obj) is False
    assert result_obj.message == "NoReachableDeviceException: No reachable Sonos devices"
