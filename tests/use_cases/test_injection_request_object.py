from snipssonos.use_cases.request_objects import InjectEntitiesRequestFactory


def test_build_injection_request_object_from_empty_dict():
    injection_request = InjectEntitiesRequestFactory.from_dict(dict())
    assert bool(injection_request) is False


def test_build_injection_request_object_from_non_string_value():
    adict = {
        "entity_name": 1
    }
    injection_request = InjectEntitiesRequestFactory.from_dict(adict)
    assert bool(injection_request) is False


def test_build_injection_request_object_valid():
    adict = {
        "entity_name": "snips/artist"
    }
    injection_request = InjectEntitiesRequestFactory.from_dict(adict)
    assert bool(injection_request) is True

