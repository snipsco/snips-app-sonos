import pytest
from mock import mock


from snipssonos.entities.device import Device
from snipssonos.entities.playlist import Playlist
from snipssonos.use_cases.play.playlist import PlayPlaylistUseCase
from snipssonos.use_cases.request_objects import PlayPlaylistRequestFactory

from snipssonos.services.feedback.feedback_service import FeedbackService
from snipssonos.services.feedback.feedback_messages import FR_TTS_GENERIC_ERROR, FR_TTS_PLAYING_PLAYLIST_TEMPLATE

@pytest.fixture
def connected_device():
    return Device(
        name="Anthony's Sonos",
        identifier="RINCON_XXXX",
        volume=10
    )

@pytest.fixture
def feedback_service():
    return FeedbackService('fr')


def test_use_case_with_track_name_and_empty_parameter_success_tts(connected_device, feedback_service):
    req_obj = PlayPlaylistRequestFactory.from_dict(
        {'playlist_name': 'vibing'})
    mock_device_discovery_service = mock.Mock()
    mock_device_discovery_service.get.return_value = connected_device  # We mock the device discovery service

    mock_music_search_service = mock.Mock()

    mock_music_search_service.search_playlist.return_value = [Playlist("URI", "vibing")]

    mock_music_playback_service = mock.Mock()

    use_case = PlayPlaylistUseCase(mock_device_discovery_service, mock_music_search_service,
                                   mock_music_playback_service, feedback_service)
    response = use_case.execute(req_obj)

    assert response.feedback == FR_TTS_PLAYING_PLAYLIST_TEMPLATE.format("vibing")


def test_use_case_with_track_name_failure_tts(connected_device, feedback_service):
    req_obj = PlayPlaylistRequestFactory.from_dict(
        {'playlist_name': 'vibing'})
    mock_device_discovery_service = mock.Mock()
    mock_device_discovery_service.get.return_value = connected_device  # We mock the device discovery service

    mock_music_search_service = mock.Mock()

    mock_music_search_service.search_playlist.return_value = []

    mock_music_playback_service = mock.Mock()

    use_case = PlayPlaylistUseCase(mock_device_discovery_service, mock_music_search_service,
                                   mock_music_playback_service, feedback_service)
    response = use_case.execute(req_obj)

    assert response.message == FR_TTS_GENERIC_ERROR
