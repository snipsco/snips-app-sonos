from mock import mock

from snipssonos.shared.use_case import UseCase
from snipssonos.shared.request_object import InvalidRequestObject, ValidRequestObject
from snipssonos.shared.response_object import ResponseFailure


def test_use_case_cannot_process_valid_requests():
    valid_request_object = ValidRequestObject()
    use_case = UseCase()
    response = use_case.execute(valid_request_object)

    assert not response
    assert isinstance(response, ResponseFailure)


def test_use_case_can_process_invalid_requests_and_returns_response_failure():
    invalid_request_object = InvalidRequestObject()
    invalid_request_object.add_error('param', 'value','type')

    use_case = UseCase()
    response = use_case.execute(invalid_request_object)

    assert not response
    assert response.type == ResponseFailure.PARAMETERS_ERROR


def test_use_case_can_manage_generic_exception_from_process_request():
    use_case = UseCase()

    class TestException(Exception):
        pass

    use_case.process_request = mock.Mock()
    use_case.process_request.side_effect = TestException("somemessage")

    response = use_case.execute(mock.Mock)

    assert not response
    assert response.type == ResponseFailure.SYSTEM_ERROR
    assert response.message == 'TestException: somemessage'
