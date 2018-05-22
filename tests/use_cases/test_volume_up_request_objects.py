from snipssonos.use_cases import request_objects as reqo

def test_build_volume_up_request_object_without_params():
    req = reqo.VolumeUpRequestObject()

    assert bool(req) is True


def test_build_volume_up_request_object_from_empty_dict():
    req = reqo.VolumeUpRequestObject.from_dict({})

    assert bool(req) is True