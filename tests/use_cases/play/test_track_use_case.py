import pytest
from mock import mock

from snipssonos.shared.request_object import InvalidRequestObject, ValidRequestObject
from snipssonos.shared.response_object import ResponseFailure, ResponseSuccess
from snipssonos.exceptions import NoReachableDeviceException, MusicSearchCredentialsError, \
    MusicSearchProviderConnectionError

from snipssonos.entities.device import Device
from snipssonos.entities.track import Track
from snipssonos.use_cases.play.track import PlayTrackUseCase
from snipssonos.use_cases.request_objects import PlayTrackRequestFactory

from snipssonos.services.feedback.feedback_service import FeedbackService
from snipssonos.services.feedback.feedback_messages import FR_TTS_GENERIC_ERROR, FR_TTS_PLAYING_TRACK_TEMPLATE

pytestmark = pytest.mark.skip("all tests still WIP")

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


def test_use_case_empty_parameters(connected_device, feedback_service):
    empty_params_req_object = PlayTrackRequestFactory.from_dict({})
    mock_device_discovery_service = mock.Mock()
    mock_music_search_service = mock.Mock()
    mock_music_playback_service = mock.Mock()

    use_case = PlayTrackUseCase(mock_device_discovery_service, mock_music_search_service,
                                mock_music_playback_service, feedback_service)

    response = use_case.execute(empty_params_req_object)
    assert isinstance(empty_params_req_object, InvalidRequestObject)
    assert isinstance(response, ResponseFailure)
    assert response.type == ResponseFailure.PARAMETERS_ERROR


def test_use_case_no_reachable_device(connected_device, feedback_service):
    mock_device_discovery_service = mock.Mock()
    mock_device_discovery_service.get.side_effect = NoReachableDeviceException(
        "No reachable Sonos devices")  # We mock the device discovery service

    mock_music_search_service = mock.Mock()
    mock_music_playback_service = mock.Mock()

    req_object = PlayTrackRequestFactory.from_dict({'track_name': "I thought it was you"})
    use_case = PlayTrackUseCase(mock_device_discovery_service, mock_music_search_service,
                                mock_music_playback_service, feedback_service)

    response = use_case.execute(req_object)

    assert isinstance(req_object, ValidRequestObject)
    assert isinstance(response, ResponseFailure)
    assert response.type == ResponseFailure.SYSTEM_ERROR
    assert response.message == "NoReachableDeviceException: No reachable Sonos devices"


def test_wrong_credentials(connected_device, feedback_service):
    req_object = PlayTrackRequestFactory.from_dict({'track_name': "I thought it was you"})
    mock_device_discovery_service = mock.Mock()
    mock_device_discovery_service.get.return_value = connected_device  # We mock the device discovery service

    mock_music_search_service = mock.Mock()
    mock_music_search_service.search_track.side_effect = MusicSearchCredentialsError("Wrong credentials")
    mock_music_playback_service = mock.Mock()

    use_case = PlayTrackUseCase(mock_device_discovery_service, mock_music_search_service,
                                mock_music_playback_service, feedback_service)

    response = use_case.execute(req_object)

    assert isinstance(req_object, ValidRequestObject)
    assert isinstance(response, ResponseFailure)
    assert response.type == ResponseFailure.SYSTEM_ERROR
    assert response.message == "MusicSearchCredentialsError: Wrong credentials"


def test_music_search_service_not_responding(connected_device, feedback_service):
    req_obj = PlayTrackRequestFactory.from_dict({'track_name': "I thought it was you"})
    mock_device_discovery_service = mock.Mock()
    mock_device_discovery_service.get.return_value = connected_device  # We mock the device discovery service

    mock_music_search_service = mock.Mock()
    mock_music_search_service.client = mock.Mock()
    mock_music_search_service.client.execute_query.side_effect = MusicSearchProviderConnectionError()
    mock_music_playback_service = mock.Mock()

    use_case = PlayTrackUseCase(mock_device_discovery_service, mock_music_search_service,
                                mock_music_playback_service, feedback_service)

    response = use_case.execute(req_obj)
    assert isinstance(response, ResponseFailure)
    assert isinstance(req_obj, ValidRequestObject)
    assert response.type == ResponseFailure.SYSTEM_ERROR


def test_use_case_with_wrong_type_parameter(connected_device, feedback_service):
    req_obj = PlayTrackRequestFactory.from_dict({'wrong_key': "This is on purpose"})
    mock_device_discovery_service = mock.Mock()
    mock_device_discovery_service.get.return_value = connected_device  # We mock the device discovery service
    mock_music_search_service = mock.Mock()
    mock_music_playback_service = mock.Mock()

    use_case = PlayTrackUseCase(mock_device_discovery_service, mock_music_search_service,
                                mock_music_playback_service, feedback_service)

    response = use_case.execute(req_obj)
    assert isinstance(response, ResponseFailure)
    assert isinstance(req_obj, InvalidRequestObject)


def test_use_case_with_track_name(connected_device, feedback_service):
    req_obj = PlayTrackRequestFactory.from_dict({'track_name': "I'm upset"})
    mock_device_discovery_service = mock.Mock()
    mock_device_discovery_service.get.return_value = connected_device  # We mock the device discovery service

    mock_music_search_service = mock.Mock()
    mock_music_search_service.search_track.return_value = [Track("URI", "I'm upset")]

    mock_music_playback_service = mock.Mock()

    use_case = PlayTrackUseCase(mock_device_discovery_service, mock_music_search_service,
                                mock_music_playback_service, feedback_service)
    response = use_case.execute(req_obj)

    assert isinstance(req_obj, ValidRequestObject)
    assert isinstance(response, ResponseSuccess)
    mock_music_search_service.search_track.assert_called_with("I'm upset")


def test_use_case_with_track_name_and_playlist_name(connected_device, feedback_service):
    req_obj = PlayTrackRequestFactory.from_dict({'track_name': "I'm upset", 'playlist_name': 'Discover Weekly'})
    mock_device_discovery_service = mock.Mock()
    mock_device_discovery_service.get.return_value = connected_device  # We mock the device discovery service

    mock_music_search_service = mock.Mock()
    mock_music_search_service.search_track_for_playlist.return_value = [Track("URI", "I'm upset")]

    mock_music_playback_service = mock.Mock()

    use_case = PlayTrackUseCase(mock_device_discovery_service, mock_music_search_service,
                                mock_music_playback_service, feedback_service)
    response = use_case.execute(req_obj)

    assert isinstance(req_obj, ValidRequestObject)
    assert isinstance(response, ResponseSuccess)
    mock_music_search_service.search_track_for_playlist.assert_called_with("I'm upset", "Discover Weekly")


def test_use_case_with_track_name_and_artist_name(connected_device, feedback_service):
    req_obj = PlayTrackRequestFactory.from_dict({'track_name': "I'm upset", 'artist_name': 'Drake'})
    mock_device_discovery_service = mock.Mock()
    mock_device_discovery_service.get.return_value = connected_device  # We mock the device discovery service

    mock_music_search_service = mock.Mock()
    mock_music_search_service.search_track_for_artist.return_value = [Track("URI", "I'm upset")]

    mock_music_playback_service = mock.Mock()

    use_case = PlayTrackUseCase(mock_device_discovery_service, mock_music_search_service,
                                mock_music_playback_service, feedback_service)
    response = use_case.execute(req_obj)

    assert isinstance(req_obj, ValidRequestObject)
    assert isinstance(response, ResponseSuccess)
    mock_music_search_service.search_track_for_artist.assert_called_with("I'm upset", "Drake")


def test_use_case_with_track_name_and_artist_name_and_playlist_name(connected_device, feedback_service):
    req_obj = PlayTrackRequestFactory.from_dict(
        {'track_name': "I'm upset", 'artist_name': 'Drake', 'playlist_name': 'Discover Weekly'})
    mock_device_discovery_service = mock.Mock()
    mock_device_discovery_service.get.return_value = connected_device  # We mock the device discovery service

    mock_music_search_service = mock.Mock()
    mock_music_search_service.search_track_for_artist_and_for_playlist.return_value = [Track("URI", "I'm upset")]

    mock_music_playback_service = mock.Mock()

    use_case = PlayTrackUseCase(mock_device_discovery_service, mock_music_search_service,
                                mock_music_playback_service, feedback_service)
    response = use_case.execute(req_obj)

    assert isinstance(req_obj, ValidRequestObject)
    assert isinstance(response, ResponseSuccess)
    mock_music_search_service.search_track_for_artist_and_for_playlist.assert_called_with("I'm upset", "Drake",
                                                                                          "Discover Weekly")  # TODO : Complete me


def test_use_case_with_track_name_and_album_name(connected_device, feedback_service):
    req_obj = PlayTrackRequestFactory.from_dict({'track_name': "I'm upset", 'album_name': 'Scorpion'})
    mock_device_discovery_service = mock.Mock()
    mock_device_discovery_service.get.return_value = connected_device  # We mock the device discovery service

    mock_music_search_service = mock.Mock()
    mock_music_search_service.search_track_for_album.return_value = [Track("URI", "I'm upset")]

    mock_music_playback_service = mock.Mock()

    use_case = PlayTrackUseCase(mock_device_discovery_service, mock_music_search_service,
                                mock_music_playback_service, feedback_service)
    response = use_case.execute(req_obj)

    assert isinstance(req_obj, ValidRequestObject)
    assert isinstance(response, ResponseSuccess)
    mock_music_search_service.search_track_for_album.assert_called_with("I'm upset", "Scorpion")


def test_use_case_with_track_name_album_name_and_playlist_name(connected_device, feedback_service):
    req_obj = PlayTrackRequestFactory.from_dict(
        {'track_name': "I'm upset", 'album_name': 'Scorpion', 'playlist_name': 'Discover Weekly'})
    mock_device_discovery_service = mock.Mock()
    mock_device_discovery_service.get.return_value = connected_device  # We mock the device discovery service

    mock_music_search_service = mock.Mock()
    mock_music_search_service.search_track_for_album_and_for_playlist.return_value = [Track("URI", "I'm upset")]

    mock_music_playback_service = mock.Mock()

    use_case = PlayTrackUseCase(mock_device_discovery_service, mock_music_search_service,
                                mock_music_playback_service, feedback_service)
    response = use_case.execute(req_obj)

    assert isinstance(req_obj, ValidRequestObject)
    assert isinstance(response, ResponseSuccess)
    mock_music_search_service.search_track_for_album_and_for_playlist.assert_called_with("I'm upset", "Scorpion",
                                                                                         "Discover Weekly")


def test_use_case_with_track_name_album_name_and_artist_name(connected_device, feedback_service):
    req_obj = PlayTrackRequestFactory.from_dict(
        {'track_name': "I'm upset", 'album_name': 'Scorpion', 'artist_name': 'Drake'})
    mock_device_discovery_service = mock.Mock()
    mock_device_discovery_service.get.return_value = connected_device  # We mock the device discovery service

    mock_music_search_service = mock.Mock()
    mock_music_search_service.search_track_for_album_and_for_artist.return_value = [Track("URI", "I'm upset")]

    mock_music_playback_service = mock.Mock()

    use_case = PlayTrackUseCase(mock_device_discovery_service, mock_music_search_service,
                                mock_music_playback_service, feedback_service)
    response = use_case.execute(req_obj)

    assert isinstance(req_obj, ValidRequestObject)
    assert isinstance(response, ResponseSuccess)
    mock_music_search_service.search_track_for_album_and_for_artist.assert_called_with("I'm upset", "Scorpion", "Drake")


def test_use_case_with_track_name_album_name_artist_name_and_playlist_name(connected_device, feedback_service):
    req_obj = PlayTrackRequestFactory.from_dict(
        {'track_name': "I'm upset", 'album_name': 'Scorpion', 'artist_name': 'Drake',
         'playlist_name': 'Discover Weekly'})
    mock_device_discovery_service = mock.Mock()
    mock_device_discovery_service.get.return_value = connected_device  # We mock the device discovery service

    mock_music_search_service = mock.Mock()
    mock_music_search_service.search_track_for_album_and_for_artist_and_for_playlist.return_value = [
        Track("URI", "I'm upset")]

    mock_music_playback_service = mock.Mock()

    use_case = PlayTrackUseCase(mock_device_discovery_service, mock_music_search_service,
                                mock_music_playback_service, feedback_service)
    response = use_case.execute(req_obj)

    assert isinstance(req_obj, ValidRequestObject)
    assert isinstance(response, ResponseSuccess)
    mock_music_search_service.search_track_for_album_and_for_artist_and_for_playlist.assert_called_with("I'm upset",
                                                                                                        "Scorpion",
                                                                                                        "Drake",
                                                                                                        "Discover Weekly")


def test_use_case_with_empty_track_name(connected_device, feedback_service):
    req_obj = PlayTrackRequestFactory.from_dict({'track_name': ""})
    mock_device_discovery_service = mock.Mock()
    mock_device_discovery_service.get.return_value = connected_device  # We mock the device discovery service

    mock_music_search_service = mock.Mock()
    mock_music_playback_service = mock.Mock()

    use_case = PlayTrackUseCase(mock_device_discovery_service, mock_music_search_service,
                                mock_music_playback_service, feedback_service)
    response = use_case.execute(req_obj)

    assert isinstance(req_obj, InvalidRequestObject)
    assert isinstance(response, ResponseFailure)


def test_use_case_with_track_name_and_empty_parameter(connected_device, feedback_service):
    req_obj = PlayTrackRequestFactory.from_dict(
        {'track_name': "I'm upset", 'album_name': '', 'artist_name': '',
         'playlist_name': ''})
    mock_device_discovery_service = mock.Mock()
    mock_device_discovery_service.get.return_value = connected_device  # We mock the device discovery service

    mock_music_search_service = mock.Mock()
    mock_music_search_service.search_track_for_album_and_for_artist_and_for_playlist.return_value = [
        Track("URI", "I'm upset")]

    mock_music_playback_service = mock.Mock()

    use_case = PlayTrackUseCase(mock_device_discovery_service, mock_music_search_service,
                                mock_music_playback_service, feedback_service)
    response = use_case.execute(req_obj)

    assert isinstance(req_obj, ValidRequestObject)
    assert isinstance(response, ResponseSuccess)
    mock_music_search_service.search_track.assert_called_with("I'm upset")


def test_use_case_with_track_name_and_empty_parameter_success_tts(connected_device, feedback_service):
    req_obj = PlayTrackRequestFactory.from_dict(
        {'track_name': "I'm upset", 'album_name': '', 'artist_name': '',
         'playlist_name': ''})
    mock_device_discovery_service = mock.Mock()
    mock_device_discovery_service.get.return_value = connected_device  # We mock the device discovery service

    mock_music_search_service = mock.Mock()

    mock_music_search_service.search_track.return_value = [Track("URI", "I'm upset", "Drake")]

    mock_music_playback_service = mock.Mock()

    use_case = PlayTrackUseCase(mock_device_discovery_service, mock_music_search_service,
                                mock_music_playback_service, feedback_service)
    response = use_case.execute(req_obj)

    assert response.feedback == FR_TTS_PLAYING_TRACK_TEMPLATE.format("I'm upset", "Drake")


def test_use_case_with_track_name_failure_tts(connected_device, feedback_service):
    req_obj = PlayTrackRequestFactory.from_dict(
        {'track_name': "I'm upset"})
    mock_device_discovery_service = mock.Mock()
    mock_device_discovery_service.get.return_value = connected_device  # We mock the device discovery service

    mock_music_search_service = mock.Mock()

    mock_music_search_service.search_track.return_value = []

    mock_music_playback_service = mock.Mock()

    use_case = PlayTrackUseCase(mock_device_discovery_service, mock_music_search_service,
                                mock_music_playback_service, feedback_service)
    response = use_case.execute(req_obj)

    assert response.message == FR_TTS_GENERIC_ERROR

def test_use_case_feedback(connected_device, feedback_service):
    assert False
