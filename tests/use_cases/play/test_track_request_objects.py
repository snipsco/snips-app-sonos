import pytest

from snipssonos.use_cases import request_objects as reqo
from snipssonos.exceptions import RequestObjectInitializationException


def test_build_play_track_request_object_without_params():
    with pytest.raises(RequestObjectInitializationException):
        reqo.PlayTrackRequestObject(None, None, None, None)


def test_build_play_track_request_object_from_empty_dict():
    play_track_request = reqo.PlayTrackRequestFactory.from_dict(dict())

    assert bool(play_track_request) is False


def test_returns_invalid_request_object_for_wrong_param_type_dictionary():
    play_track_request = reqo.PlayTrackRequestFactory.from_dict({'track_name': 1})

    assert bool(play_track_request) is False
