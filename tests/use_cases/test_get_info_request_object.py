from snipssonos.use_cases import request_objects as reqo


def test_build_get_track_info_request_object_without_params():
    req = reqo.GetTrackInfoRequestFactory()

    assert bool(req) is True


def test_build_get_track_info_request_object_from_empty_dict():
    req = reqo.GetTrackInfoRequestFactory.from_dict({})

    assert bool(req) is True
