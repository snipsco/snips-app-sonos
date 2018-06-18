import mock
import pytest
import requests

from snipssonos.entities.device import Device
from snipssonos.services.node.device_discovery_service import NodeDeviceDiscoveryService
from snipssonos.exceptions import DeviceParsingException, NoReachableDeviceException


@pytest.fixture
def connected_device():
    return Device.from_dict({
        'identifier': 'RINCON_7828CA10127001400',
        'name': 'Antho Room',
        'volume': 18
    })


def test_device_discovery_service_initialization():
    discovery_service = NodeDeviceDiscoveryService()

    assert discovery_service.PORT == NodeDeviceDiscoveryService.PORT
    assert discovery_service.HOST == NodeDeviceDiscoveryService.HOST
    assert discovery_service.PROTOCOL == NodeDeviceDiscoveryService.PROTOCOL


def test_generate_correct_url_query_for_get_method():
    discovery_service = NodeDeviceDiscoveryService()

    expected_query = "http://localhost:5005/zones/"
    actual_query = discovery_service.generate_get_query()

    assert expected_query == actual_query


def test_parses_correct_device_from_input_json():
    discovery_service = NodeDeviceDiscoveryService()
    json_response = """[
    {
        "uuid": "RINCON_7828CA10127001400",
        "coordinator": {
            "uuid": "RINCON_7828CA10127001400",
            "state": {
                "volume": 17,
                "mute": false,
                "equalizer": {
                    "bass": 0,
                    "treble": 0,
                    "loudness": true
                },
                "currentTrack": {
                    "artist": "Fatback Band",
                    "title": "Chillin' Out",
                    "album": "14 Karat",
                    "albumArtUri": "/getaa?s=1&u=x-sonos-spotify%3aspotify%253atrack%253a1bAeucHM9U9RJBJM3bPIGU%3fsid%3d9%26flags%3d8224%26sn%3d2",
                    "duration": 341,
                    "uri": "x-sonos-spotify:spotify%3atrack%3a1bAeucHM9U9RJBJM3bPIGU?sid=9&flags=8224&sn=2",
                    "type": "track",
                    "stationName": "",
                    "absoluteAlbumArtUri": "http://192.168.173.215:1400/getaa?s=1&u=x-sonos-spotify%3aspotify%253atrack%253a1bAeucHM9U9RJBJM3bPIGU%3fsid%3d9%26flags%3d8224%26sn%3d2"
                },
                "nextTrack": {
                    "artist": "",
                    "title": "",
                    "album": "",
                    "albumArtUri": "",
                    "duration": 0,
                    "uri": ""
                },
                "trackNo": 2,
                "elapsedTime": 37,
                "elapsedTimeFormatted": "00:00:37",
                "playbackState": "PAUSED_PLAYBACK",
                "playMode": {
                    "repeat": "none",
                    "shuffle": false,
                    "crossfade": false
                }
            },
            "roomName": "Antho Room",
            "coordinator": "RINCON_7828CA10127001400",
            "groupState": {
                "volume": 17,
                "mute": false
            }
        },
        "members": [
            {
                "uuid": "RINCON_7828CA10127001400",
                "state": {
                    "volume": 17,
                    "mute": false,
                    "equalizer": {
                        "bass": 0,
                        "treble": 0,
                        "loudness": true
                    },
                    "currentTrack": {
                        "artist": "Fatback Band",
                        "title": "Chillin' Out",
                        "album": "14 Karat",
                        "albumArtUri": "/getaa?s=1&u=x-sonos-spotify%3aspotify%253atrack%253a1bAeucHM9U9RJBJM3bPIGU%3fsid%3d9%26flags%3d8224%26sn%3d2",
                        "duration": 341,
                        "uri": "x-sonos-spotify:spotify%3atrack%3a1bAeucHM9U9RJBJM3bPIGU?sid=9&flags=8224&sn=2",
                        "type": "track",
                        "stationName": "",
                        "absoluteAlbumArtUri": "http://192.168.173.215:1400/getaa?s=1&u=x-sonos-spotify%3aspotify%253atrack%253a1bAeucHM9U9RJBJM3bPIGU%3fsid%3d9%26flags%3d8224%26sn%3d2"
                    },
                    "nextTrack": {
                        "artist": "",
                        "title": "",
                        "album": "",
                        "albumArtUri": "",
                        "duration": 0,
                        "uri": ""
                    },
                    "trackNo": 2,
                    "elapsedTime": 37,
                    "elapsedTimeFormatted": "00:00:37",
                    "playbackState": "PAUSED_PLAYBACK",
                    "playMode": {
                        "repeat": "none",
                        "shuffle": false,
                        "crossfade": false
                    }
                },
                "roomName": "Antho Room",
                "coordinator": "RINCON_7828CA10127001400",
                "groupState": {
                    "volume": 17,
                    "mute": false
                }
            }
        ]
    }
]"""
    devices = discovery_service.parse_devices(json_response)

    assert len(devices) == 1
    assert devices[0].identifier == "RINCON_7828CA10127001400"
    assert devices[0].name == "Antho Room"
    assert devices[0].volume == 17


def test_parsing_invalid_json_raises_exception():
    discovery_service = NodeDeviceDiscoveryService()
    json_response = """[
        {
            "members": [
                {
                    "uuuid": "RINCON_7828CA10127001400",
                    "state": {
                        "volume": 17,
                        "mute": false,
                        "equalizer": {
                            "bass": 0,
                            "treble": 0,
                            "loudness": true
                        },
                        "currentTrack": {
                            "artist": "Fatback Band",
                            "title": "Chillin' Out",
                            "album": "14 Karat",
                            "albumArtUri": "/getaa?s=1&u=x-sonos-spotify%3aspotify%253atrack%253a1bAeucHM9U9RJBJM3bPIGU%3fsid%3d9%26flags%3d8224%26sn%3d2",
                            "duration": 341,
                            "uri": "x-sonos-spotify:spotify%3atrack%3a1bAeucHM9U9RJBJM3bPIGU?sid=9&flags=8224&sn=2",
                            "type": "track",
                            "stationName": "",
                            "absoluteAlbumArtUri": "http://192.168.173.215:1400/getaa?s=1&u=x-sonos-spotify%3aspotify%253atrack%253a1bAeucHM9U9RJBJM3bPIGU%3fsid%3d9%26flags%3d8224%26sn%3d2"
                        },
                        "nextTrack": {
                            "artist": "",
                            "title": "",
                            "album": "",
                            "albumArtUri": "",
                            "duration": 0,
                            "uri": ""
                        },
                        "trackNo": 2,
                        "elapsedTime": 37,
                        "elapsedTimeFormatted": "00:00:37",
                        "playbackState": "PAUSED_PLAYBACK",
                        "playMode": {
                            "repeat": "none",
                            "shuffle": false,
                            "crossfade": false
                        }
                    },
                    "roomName": "Antho Room",
                    "coordinator": "RINCON_7828CA10127001400",
                    "groupState": {
                        "volume": 17,
                        "mute": false
                    }
                }
            ]
        }
    ]"""
    with pytest.raises(DeviceParsingException):
        discovery_service.parse_devices(json_response)


def test_parsing_json_with_empty_members():
    discovery_service = NodeDeviceDiscoveryService()
    json_response = """[
        {"members": []}]"""

    devices = discovery_service.parse_devices(json_response)

    assert len(devices) == 0


@mock.patch.object(NodeDeviceDiscoveryService, 'get_devices')
def test_get_method_returns_first_occurrence(mocked_get_devices, connected_device):
    discovery_service = NodeDeviceDiscoveryService()
    mocked_get_devices.return_value = [connected_device]

    assert discovery_service.get().name == connected_device.name
    assert discovery_service.get().identifier == connected_device.identifier
    assert discovery_service.get().volume == connected_device.volume


@mock.patch('snipssonos.services.node.device_discovery_service.requests')
def test_get_method_performs_correct_api_query(mocked_requests):
    discovery_device = NodeDeviceDiscoveryService()

    discovery_device.execute_query()
    actual_query = discovery_device.generate_get_query()
    mocked_requests.get.assert_called_with(actual_query)


@mock.patch('snipssonos.services.node.device_discovery_service.requests')
def test_unreachable_device_raises_exception(mocked_requests):
    discovery_device = NodeDeviceDiscoveryService()

    mocked_response_object = mock.create_autospec(requests.Response)
    mocked_response_object.ok = False

    mocked_requests.get.return_value = mocked_response_object

    with pytest.raises(NoReachableDeviceException):
        discovery_device.execute_query()
