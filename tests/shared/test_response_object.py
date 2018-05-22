import pytest

from snipssonos.shared import response_object as reso
from snipssonos.use_cases import request_objects as reqo


@pytest.fixture
def response_value():
    return {'key' : ['value1', 'value2']}

@pytest.fixture
def response_type():
    return 'ResponseError'

@pytest.fixture
def response_message():
    return 'This is a response error'

def test_response_success_is_true(response_value):
    r = reso.ResponseSuccess(None)

    assert bool(r) is True

def test_response_failure_is_false(response_type, response_message):
    r = reso.ResponseFailure(response_type, response_message)

    assert bool(r) is False

def test_response_success_contains_value(response_value):
    r = reso.ResponseSuccess(response_value)

    assert r.value == response_value

def test_response_failure_contains_message(response_type, response_message):
    r = reso.ResponseFailure(response_type, response_message)

    assert r.type == response_type
    assert r.message == response_message


def test_response_failure_contains_value(response_type, response_message):
    r = reso.ResponseFailure(response_type, response_message)

    assert r.value == {'type': response_type, 'message': response_message}


def test_response_failure_initialization_with_exception(response_type):
    error_message = "An error message"
    response = reso.ResponseFailure(response_type, Exception(error_message))

    assert bool(response) is False

    assert response.type == response_type
    assert response.message == "Exception: {}".format(error_message)

def test_response_failure_from_invalid_request_object():
    response = reso.ResponseFailure.build_from_invalid_request_object(reqo.InvalidRequestObject())

    assert bool(response) is False

def test_response_failure_from_invalid_request_object_with_errors():
    request_object = reqo.InvalidRequestObject()

    request_object.add_error('path', 'is mandatory')
    request_object.add_error('path', 'cannot be blank')

    response = reso.ResponseFailure.build_from_invalid_request_object(request_object)

    assert bool(response) is False
    assert response.type == reso.ResponseFailure.PARAMETERS_ERROR
    assert response.message == "path: is mandatory\npath: cannot be blank"


def test_response_failure_build_resource_error():
    response = reso.ResponseFailure.build_resource_error("test message")

    assert bool(response) is False
    assert response.type == reso.ResponseFailure.RESOURCE_ERROR
    assert response.message == "test message"




