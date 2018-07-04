import pytest
from mock import mock

from snipssonos.shared.request_object import InvalidRequestObject, ValidRequestObject
from snipssonos.shared.response_object import ResponseFailure
from snipssonos.exceptions import NoReachableDeviceException

from snipssonos.use_cases.play.track import PlayTrackUseCase
from snipssonos.use_cases.request_objects import PlayTrackRequestFactory


def test_use_case_empty_parameters():
    empty_params_req_object = PlayTrackRequestFactory.from_dict({})
    mock_device_discovery_service = mock.Mock()
    mock_music_search_service = mock.Mock()
    mock_music_playback_service = mock.Mock()

    use_case = PlayTrackUseCase(mock_device_discovery_service, mock_music_search_service, mock_music_playback_service)

    response = use_case.execute(empty_params_req_object)
    assert isinstance(empty_params_req_object, InvalidRequestObject)
    assert isinstance(response, ResponseFailure)


def test_use_case_no_reachable_device():
    mock_device_discovery_service = mock.Mock()
    mock_device_discovery_service.get.side_effect = NoReachableDeviceException("No reachable Sonos devices")  # We mock the device discovery service

    mock_music_search_service = mock.Mock()
    mock_music_playback_service = mock.Mock()

    req_object = PlayTrackRequestFactory.from_dict({'track_name': "I thought it was you"})
    use_case = PlayTrackUseCase(mock_device_discovery_service, mock_music_search_service, mock_music_playback_service)

    response = use_case.execute(req_object)

    assert isinstance(req_object, ValidRequestObject)
    assert isinstance(response, ResponseFailure)


@pytest.mark.skip(reason="Waiting for next iteration to move parameters validation to constructor")
def test_wrong_credentials():
    assert True is False


@pytest.mark.skip(reason="Waiting for next iteration to move parameters validation to constructor")
def test_music_service_not_responding():
    assert True is False


@pytest.mark.skip(reason="Waiting for next iteration to move parameters validation to constructor")
def test_use_case_with_wrong_type_parameter():
    assert True is False


@pytest.mark.skip(reason="Waiting for next iteration to move parameters validation to constructor")
def test_use_case_with_track_name():
    assert True is False


@pytest.mark.skip(reason="Waiting for next iteration to move parameters validation to constructor")
def test_use_case_with_track_name_and_playlist_name():
    assert True is False


@pytest.mark.skip(reason="Waiting for next iteration to move parameters validation to constructor")
def test_use_case_with_track_name_and_artist_name():
    assert True is False


@pytest.mark.skip(reason="Waiting for next iteration to move parameters validation to constructor")
def test_use_case_with_track_name_and_artist_name_and_playlist_name():
    assert True is False


@pytest.mark.skip(reason="Waiting for next iteration to move parameters validation to constructor")
def test_use_case_with_track_name_and_album_name():
    assert True is False


@pytest.mark.skip(reason="Waiting for next iteration to move parameters validation to constructor")
def test_use_case_with_track_name_album_name_and_playlist_name():
    assert True is False


@pytest.mark.skip(reason="Waiting for next iteration to move parameters validation to constructor")
def test_use_case_with_track_name_album_name_and_artist_name():
    assert True is False


@pytest.mark.skip(reason="Waiting for next iteration to move parameters validation to constructor")
def test_use_case_with_track_name_album_name_artist_name_and_playlist_name():
    assert True is False


@pytest.mark.skip(reason="Waiting for next iteration to move parameters validation to constructor")
def test_use_case_with_empty_track_name():
    assert True is False


@pytest.mark.skip(reason="Waiting for next iteration to move parameters validation to constructor")
def test_use_case_with_track_name_and_empty_parameter():
    assert True is False
