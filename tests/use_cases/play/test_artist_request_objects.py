import pytest

from snipssonos.use_cases import request_objects as reqo

def test_build_play_track_request_object_from_empty_dict():
    play_track_request = reqo.PlayArtistRequestFactory.from_dict(dict())

    assert bool(play_track_request) is False
