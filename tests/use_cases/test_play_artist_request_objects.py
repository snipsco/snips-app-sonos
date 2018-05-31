import pytest

from snipssonos.use_cases import request_objects as reqo


@pytest.mark.skip(reason="Waiting for next iteration to move parameters validation to constructor")
def test_build_play_artist_request_object_without_params():
    play_track_request = reqo.PlayArtistRequestObject(None, None)

    assert bool(play_track_request) is False


def test_build_play_track_request_object_from_empty_dict():
    play_track_request = reqo.PlayArtistRequestObject.from_dict(dict())

    assert bool(play_track_request) is False



