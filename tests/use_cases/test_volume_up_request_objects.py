import pytest

from snipssonos.use_cases import request_objects as reqo
from snipssonos.shared.request_object import InvalidRequestObject, ValidRequestObject


def test_build_volume_up_request_object_without_params():
    req = reqo.VolumeUpRequestObject()

    assert bool(req) is True


def test_build_volume_up_request_object_from_empty_dict():
    req = reqo.VolumeUpRequestObject.from_dict({})

    assert bool(req) is True


def test_returns_invalid_request_object_for_wrong_params_dictionary():
    req = reqo.VolumeUpRequestObject.from_dict({
        'volume_increase': 'loud'
    })

    assert bool(req) is False
    assert isinstance(req, InvalidRequestObject)


def test_returns_invalid_request_object_for_out_of_range_params_dictionary1():
    req = reqo.VolumeUpRequestObject.from_dict({
        'volume_increase': 1234
    })

    assert bool(req) is False
    assert isinstance(req, InvalidRequestObject)
    assert req.has_errors() is True


def test_returns_invalid_request_object_for_out_of_range_params_dictionary2():
    req = reqo.VolumeUpRequestObject.from_dict({
        'volume_increase': -123
    })

    assert bool(req) is False
    assert isinstance(req, InvalidRequestObject)
    assert req.has_errors() is True


def test_returns_invalid_request_object_for_out_of_range_params():
    req = reqo.VolumeUpRequestObject(volume_increase=1234)

    assert bool(req) is False
    assert isinstance(req, InvalidRequestObject)
    assert req.has_errors() is True


@pytest.mark.skip(reason="Waiting for next iteration to move parameters validation to constructor")
def test_returns_invalid_request_object_for_out_of_range_params():
    req = reqo.VolumeUpRequestObject(volume_increase=-1234)

    assert bool(req) is False
    assert isinstance(req, InvalidRequestObject)
    assert req.has_errors() is True


@pytest.mark.skip(reason="Waiting for next iteration to move parameters validation to constructor")
def test_returns_invalid_request_object_for_wrong_params():
    req = reqo.VolumeUpRequestObject(volume_increase="louder")

    assert bool(req) is False
    assert isinstance(req, InvalidRequestObject)
    assert req.has_errors() is True
