from snipssonos.use_cases.request_objects import InjectEntitiesRequestFactory

VALID_ENTITY_NAMES = ["artists", "tracks", "playlists"]


def test_build_injection_request_object_from_empty_dict():
    injection_request = InjectEntitiesRequestFactory.from_dict(dict())
    assert bool(injection_request) is False


def test_build_injection_request_object_from_non_string_value_for_entity_slot_name():
    adict = {
        "entities_type": {
            "artists": 1,
            "tracks": "snips/track",
            "playlists": "playlistNameFR"
        }
    }
    injection_request = InjectEntitiesRequestFactory.from_dict(adict)
    assert bool(injection_request) is False


def test_build_injection_request_object_from_non_string_value_for_entity_name():
    adict = {
        "entities_type": {
            1: "snips/artist",
            "tracks": "snips/track",
            "playlists": "playlistNameFR"
        }
    }
    injection_request = InjectEntitiesRequestFactory.from_dict(adict)
    assert bool(injection_request) is False


def test_build_injection_request_object_from_non_valid_type_for_entity_name():
    adict = {
        "entities_type": {
            "blbala": "snips/artist",
            "tracks": "snips/track",
            "playlists": "playlistNameFR"
        }
    }
    injection_request = InjectEntitiesRequestFactory.from_dict(adict)
    assert bool(injection_request) is False


def test_build_injection_request_object_valid():
    adict = {
        "entities_type": {
            "artists": "snips/artist",
            "tracks": "snips/track",
            "playlists": "playlistNameFR"
        }
    }

    injection_request = InjectEntitiesRequestFactory.from_dict(adict)
    assert bool(injection_request) is True

