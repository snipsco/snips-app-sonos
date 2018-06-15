import pytest

from snipssonos.use_cases import request_objects as reqo
from snipssonos.shared.request_object import InvalidRequestObject


def test_build_volume_down_request_object_without_params():
    req = reqo.ResumeMusicRequestObject()

    assert bool(req) is True


def test_build_volume_down_request_object_from_empty_dict():
    req = reqo.ResumeMusicRequestObject.from_dict({})

    assert bool(req) is True
