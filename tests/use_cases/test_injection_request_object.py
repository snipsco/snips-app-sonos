from snipssonos.use_cases.request_objects import InjectEntitiesRequestFactory

VALID_ENTITY_NAMES = ["artists", "tracks", "playlists"]


def test_build_injection_request_object_from_empty_dict():
    injection_request = InjectEntitiesRequestFactory.from_dict(dict())
    assert bool(injection_request) is False


def test_build_injection_request_object_from_non_string_value_for_entity_slot_name():
    adict = {
        "entity_name": VALID_ENTITY_NAMES[0],
        "entity_slot_name": 1,
    }
    injection_request = InjectEntitiesRequestFactory.from_dict(adict)
    assert bool(injection_request) is False


def test_build_injection_request_object_from_non_string_value_for_entity_name():
    adict = {
        "entity_name": 1,
        "entity_slot_name": "snips/artist",
    }
    injection_request = InjectEntitiesRequestFactory.from_dict(adict)
    assert bool(injection_request) is False


def test_build_injection_request_object_from_non_valid_type_for_entity_name():
    adict = {
        "entity_name": "blabla",
        "entity_slot_name": "snips/artist",
    }
    injection_request = InjectEntitiesRequestFactory.from_dict(adict)
    print(injection_request)
    assert bool(injection_request) is False


def test_build_injection_request_object_valid():
    adict = {
        "entity_name": VALID_ENTITY_NAMES[0],
        "entity_slot_name": "snips/artist"
    }
    injection_request = InjectEntitiesRequestFactory.from_dict(adict)
    assert bool(injection_request) is True

