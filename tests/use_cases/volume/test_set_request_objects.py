import pytest

from snipssonos.use_cases import request_objects as reqo
from snipssonos.shared.request_object import InvalidRequestObject, ValidRequestObject
from snipssonos.exceptions import RequestObjectInitializationException


def test_build_volume_set_request_object_without_params():
    with pytest.raises(RequestObjectInitializationException):
        req = reqo.VolumeSetRequestObject(None)


def test_build_volume_set_request_object_from_empty_dict():
    req = reqo.VolumeSetRequestFactory.from_dict({})

    assert bool(req) is False


def test_returns_invalid_request_object_for_wrong_params_dictionary():
    req = reqo.VolumeSetRequestFactory.from_dict({
        'volume_level': 'loud'
    })

    assert bool(req) is False
    assert isinstance(req, InvalidRequestObject)


def test_returns_invalid_request_object_for_out_of_range_params_dictionary1():
    req = reqo.VolumeSetRequestFactory.from_dict({
        'volume_level': 1234
    })

    assert bool(req) is False
    assert isinstance(req, InvalidRequestObject)
    assert req.has_errors() is True


def test_returns_invalid_request_object_for_out_of_range_params_dictionary2():
    req = reqo.VolumeSetRequestFactory.from_dict({
        'volume_level': -123
    })

    assert bool(req) is False
    assert isinstance(req, InvalidRequestObject)
    assert req.has_errors() is True


def test_returns_invalid_request_object_for_out_of_range_params():
    with pytest.raises(RequestObjectInitializationException):
        reqo.VolumeSetRequestObject(volume_level=1234)


def test_returns_invalid_request_object_for_out_of_range_params():
    with pytest.raises(RequestObjectInitializationException):
        reqo.VolumeSetRequestObject(volume_level=-1234)


def test_returns_invalid_request_object_for_wrong_params():
    with pytest.raises(RequestObjectInitializationException):
        req = reqo.VolumeSetRequestObject(volume_level="louder")
