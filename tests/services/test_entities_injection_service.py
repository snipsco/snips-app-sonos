import pytest
import mock

from snipssonos.services.entities_injection_service import EntitiesInjectionService
from snipssonos.entities.artist import Artist
from snipssonos.entities.track import Track
from snipssonos.entities.playlist import Playlist
from snipssonos.exceptions import InvalidEntitySlotName

MQTT_TOPIC_INJECT = 'hermes/asr/inject'

@pytest.fixture
def artist_data():
    data = [Artist("uri_1", "Kendrick Lamar"), Artist("uri_2", "Beyonce")]
    return data\

@pytest.fixture
def track_data():
    data = [Track("uri_1", "Kendrick Lamar"), Track("uri_2", "Beyonce")]
    return data\

@pytest.fixture
def playlist_data():
    data = [Playlist("uri_1", "Kendrick Lamar"), Playlist("uri_2", "Beyonce")]
    return data


@mock.patch('snipssonos.services.entities_injection_service.MqttClient')
def test_inject_entities_parse_artist_data_correctly(mqtt_mock, artist_data):
    hermes_host = "localhost"
    inject_entities = EntitiesInjectionService(hermes_host)

    # TODO put into a global vars file
    entity_name = "snips/artist"

    parsed_data = inject_entities.parse_data(entity_name, artist_data)
    expected_parsed_data = ["Kendrick Lamar", "Beyonce"]
    assert len(parsed_data) == len(expected_parsed_data)
    assert parsed_data == expected_parsed_data


@mock.patch('snipssonos.services.entities_injection_service.MqttClient')
def test_inject_entities_parse_track_data_correctly(mqtt_mock, artist_data, track_data):
    hermes_host = "localhost"
    inject_entities = EntitiesInjectionService(hermes_host)

    # TODO put into a global vars file
    entity_name = "snips/song"

    parsed_data = inject_entities.parse_data(entity_name, track_data)
    expected_parsed_data = ["Kendrick Lamar", "Beyonce"]
    assert len(parsed_data) == len(expected_parsed_data)
    assert parsed_data == expected_parsed_data


@mock.patch('snipssonos.services.entities_injection_service.MqttClient')
def test_inject_entities_parse_playlist_data_correctly(mqtt_mock, artist_data, track_data, playlist_data):
    hermes_host = "localhost"
    inject_entities = EntitiesInjectionService(hermes_host)

    # TODO put into a global vars file
    entity_name = "playlistNameFR"

    parsed_data = inject_entities.parse_data(entity_name, playlist_data)
    expected_parsed_data = ["Kendrick Lamar", "Beyonce"]
    assert len(parsed_data) == len(expected_parsed_data)
    assert parsed_data == expected_parsed_data


@mock.patch('snipssonos.services.entities_injection_service.MqttClient')
def test_inject_entities_parse_unknown_data_correctly(mqtt_mock):
    hermes_host = "localhost"
    inject_entities = EntitiesInjectionService(hermes_host)

    entity_name = "random_stuff"
    with pytest.raises(InvalidEntitySlotName):
        inject_entities.parse_data(entity_name, [])


@mock.patch('snipssonos.services.entities_injection_service.MqttClient')
def test_inject_entities_payload_has_correct_format(mqtt_mock, artist_data):
    hermes_host = "localhost"
    artist_entity_name = "snips/artist"

    inject_entities = EntitiesInjectionService(hermes_host)
    actual_json = inject_entities.build_payload(artist_entity_name, artist_data)

    expected_json = """{"operations": [["addFromVanilla", {"snips/artist": ["Kendrick Lamar", "Beyonce"]}]], "crossLanguage": "en"}"""
    assert expected_json == actual_json


@mock.patch('snipssonos.services.entities_injection_service.MqttClient')
def test_inject_entities_publisher_is_called_correctly(mqtt_mock, artist_data):
    mqtt_instance = mqtt_mock.return_value
    hermes_host = "localhost"
    artist_entity_name = "snips/artist"

    inject_entities = EntitiesInjectionService(hermes_host)
    payload = inject_entities.build_payload(artist_entity_name, artist_data)

    inject_entities.publish_entities(artist_entity_name, artist_data)
    mqtt_instance.publish.assert_called_with(MQTT_TOPIC_INJECT, payload)
