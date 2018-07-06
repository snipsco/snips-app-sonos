from snipssonos.use_cases import request_objects as reqo


def test_build_next_track_request_object_without_params():
    req = reqo.PreviousTrackRequestFactory()

    assert bool(req) is True


def test_build_next_track_request_object_from_empty_dict():
    req = reqo.PreviousTrackRequestFactory.from_dict({})

    assert bool(req) is True
