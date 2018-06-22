import pytest

from snipssonos.use_cases import request_objects as reqo
from snipssonos.shared.request_object import InvalidRequestObject, ValidRequestObject


def test_build_next_track_request_object_without_params():
    req = reqo.NextTrackRequestFactory()

    assert bool(req) is True


def test_build_next_track_request_object_from_empty_dict():
    req = reqo.NextTrackRequestFactory.from_dict({})

    assert bool(req) is True