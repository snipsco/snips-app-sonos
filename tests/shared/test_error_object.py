from snipssonos.shared.request_object import InvalidRequestObject, ValidRequestObject


def test_valid_request_object_is_true():
    valid_request_object = ValidRequestObject()
    assert bool(valid_request_object) is True


def test_invalid_request_object_is_false():
    invalid_request_object = InvalidRequestObject()
    assert bool(invalid_request_object) is False


def test_invalid_request_object_accepts_errors():
    invalid_request_object = InvalidRequestObject()

    invalid_request_object.add_error('param1', 'value1', 'type1')
    invalid_request_object.add_error('param2', 'value2', 'type2')
    assert bool(invalid_request_object) is False
    assert invalid_request_object.has_errors() is True
    assert len(invalid_request_object.errors) == 2
    assert invalid_request_object.errors[0]['type'] == 'type1'
