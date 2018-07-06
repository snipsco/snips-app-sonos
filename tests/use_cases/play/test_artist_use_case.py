import pytest
from mock import mock

from snipssonos.entities.device import Device

from snipssonos.use_cases.play.artist import PlayArtistUseCase
from snipssonos.use_cases.request_objects import PlayArtistRequestObject, PlayArtistRequestFactory

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

    play_artist_request = PlayArtistRequestFactory.from_dict({'artist_name' : 'Artiste'})
    result_obj = play_artist_uc.execute(play_artist_request)

    assert bool(result_obj) is False
    assert result_obj.message == "NoReachableDeviceException: No reachable Sonos devices"
