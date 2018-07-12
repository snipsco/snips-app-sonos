import pytest
from mock import mock


from snipssonos.entities.device import Device
from snipssonos.entities.album import Album
from snipssonos.use_cases.play.album import PlayAlbumUseCase
from snipssonos.use_cases.request_objects import PlayAlbumRequestFactory

from snipssonos.services.feedback.feedback_service import FeedbackService
from snipssonos.services.feedback.feedback_messages import FR_TTS_GENERIC_ERROR, FR_TTS_ALBUM_TEMPLATE

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
    req_obj = PlayAlbumRequestFactory.from_dict(
        {'album_name': 'Ash'})
    mock_device_discovery_service = mock.Mock()
    mock_device_discovery_service.get.return_value = connected_device  # We mock the device discovery service

    mock_music_search_service = mock.Mock()

    mock_music_search_service.search_album.return_value = [Album("URI", "Ash", "Ibeyi")]

    mock_music_playback_service = mock.Mock()

    use_case = PlayAlbumUseCase(mock_device_discovery_service, mock_music_search_service,
                                mock_music_playback_service, feedback_service)
    response = use_case.execute(req_obj)

    assert response.feedback == FR_TTS_ALBUM_TEMPLATE.format("Ash", "Ibeyi")


def test_use_case_with_track_name_failure_tts(connected_device, feedback_service):
    req_obj = PlayAlbumRequestFactory.from_dict(
        {'album_name': 'Ash'})
    mock_device_discovery_service = mock.Mock()
    mock_device_discovery_service.get.return_value = connected_device  # We mock the device discovery service

    mock_music_search_service = mock.Mock()

    mock_music_search_service.search_album.return_value = []

    mock_music_playback_service = mock.Mock()

    use_case = PlayAlbumUseCase(mock_device_discovery_service, mock_music_search_service,
                                mock_music_playback_service, feedback_service)
    response = use_case.execute(req_obj)

    assert response.message == FR_TTS_GENERIC_ERROR
