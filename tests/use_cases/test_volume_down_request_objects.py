import pytest

from snipssonos.use_cases import request_objects as reqo
from snipssonos.shared.request_object import InvalidRequestObject, ValidRequestObject


def test_build_volume_down_request_object_without_params():
    req = reqo.VolumeDownRequestObject()

    assert bool(req) is True


def test_build_volume_down_request_object_from_empty_dict():
    req = reqo.VolumeDownRequestObject.from_dict({})

    assert bool(req) is True


def test_returns_invalid_request_object_for_wrong_params_dictionary():
    req = reqo.VolumeDownRequestFactory.from_dict({
        'volume_decrease': 'loud'
    })

    assert bool(req) is True
    assert isinstance(req, ValidRequestObject)

