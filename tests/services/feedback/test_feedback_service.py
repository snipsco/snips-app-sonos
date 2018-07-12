import pytest
from snipssonos.shared.response_object import ResponseFailure, ResponseSuccess
from snipssonos.services.feedback.feedback_service import FeedbackService
from snipssonos.services.feedback.feedback_messages import *
import snipssonos.exceptions


def test_feedback_throws_error_non_supported_language_on_constructor():
    with pytest.raises(AttributeError):
        FeedbackService('sp')


def test_feedback_throws_error_non_supported_language_on_set():
    feedback_service = FeedbackService('fr')
    with pytest.raises(AttributeError):
        feedback_service.set_language('sp')


def test_get_fr_generic_error():
    feedback_service = FeedbackService('fr')
    assert feedback_service.get_generic_error_message() == FR_TTS_GENERIC_ERROR


def test_get_fr_short_error():
    feedback_service = FeedbackService('fr')
    assert feedback_service.get_short_error_message() == FR_TTS_SHORT_ERROR


def test_get_fr_device_discovery():
    feedback_service = FeedbackService('fr')
    assert feedback_service.get_device_discovery_message() == FR_TTS_DEVICE_DISCOVERY_SERVICE_UNREACHABLE


def test_fr_get_playlist_template():
    feedback_service = FeedbackService('fr')
    assert feedback_service.get_playlist_template() == FR_TTS_PLAYING_PLAYLIST_TEMPLATE


def test_fr_get_track_template():
    feedback_service = FeedbackService('fr')
    assert feedback_service.get_track_template() == FR_TTS_PLAYING_TRACK_TEMPLATE


def test_fr_get_album_template():
    feedback_service = FeedbackService('fr')
    assert feedback_service.get_album_template() == FR_TTS_PLAYING_ALBUM_TEMPLATE


def test_fr_get_artist_template():
    feedback_service = FeedbackService('fr')
    assert feedback_service.get_artist_template() == FR_TTS_PLAYING_ARTIST_TEMPLATE


def test_validate_language_success():
    feedback_service = FeedbackService('fr')
    assert feedback_service.validate_language('fr') is True
    assert feedback_service.validate_language('en') is True


def test_validate_language_raise_error():
    feedback_service = FeedbackService('fr')
    with pytest.raises(AttributeError):
        feedback_service.validate_language('sp')


def test_fr_get_message_from_success_response_object():
    response = ResponseSuccess(feedback="High five!")
    assert FeedbackService('fr').from_response_object(response) == "High five!"


def test_fr_get_message_from_failure_response_object_sonos_action_exception():
    response = ResponseFailure.build_system_error("", snipssonos.exceptions.SonosActionException(""))
    feedback_service = FeedbackService('fr')
    assert feedback_service.from_response_object(response) == FR_TTS_GENERIC_ERROR


def test_fr_get_message_from_failure_response_object_device_discovery():
    response = ResponseFailure.build_system_error("", snipssonos.exceptions.DeviceDiscoveryException(""))
    feedback_service = FeedbackService('fr')
    assert feedback_service.from_response_object(response) == FR_TTS_DEVICE_DISCOVERY_SERVICE_UNREACHABLE


def test_fr_get_message_from_failure_response_object_other():
    response = ResponseFailure.build_system_error("", Exception)
    feedback_service = FeedbackService('fr')
    assert feedback_service.from_response_object(response) == FR_TTS_SHORT_ERROR
