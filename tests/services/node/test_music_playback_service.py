import mock
import pytest

from snipssonos.entities.device import Device
from snipssonos.entities.track import Track
from snipssonos.services.spotify.music_playback_service import SpotifyNodeMusicPlaybackService


@pytest.fixture
def connected_device():
    return Device.from_dict({
        'identifier': 'RINCON_7828CA10127001400',
        'name': 'Antho Room',
        'volume': 18
    })


@pytest.fixture
def node_configuration():
    return {
        'global': {
            'node_music_playback_port': 5005,
            'node_music_playback_host': 'localhost',

        }
    }


def test_music_playback_service_initialization(connected_device):
    music_playback_service = SpotifyNodeMusicPlaybackService(connected_device)

    assert music_playback_service.PORT == SpotifyNodeMusicPlaybackService.PORT
    assert music_playback_service.HOST == SpotifyNodeMusicPlaybackService.HOST
    assert music_playback_service.PROTOCOL == SpotifyNodeMusicPlaybackService.PROTOCOL


def test_generate_correct_url_query_for_get_method(connected_device, node_configuration):
    music_playback_service = SpotifyNodeMusicPlaybackService(connected_device, node_configuration)

    track = Track.from_dict({'uri': 'uri'})

    expected_query = "http://localhost:5005/Antho Room/spotify/now/uri"

    actual_query = music_playback_service._generate_play_now_query(track)

    assert expected_query == actual_query


def test_generate_correct_url_query_for_queue(connected_device, node_configuration):
    music_playback_service = SpotifyNodeMusicPlaybackService(device=connected_device, CONFIGURATION=node_configuration)

    track = Track.from_dict({'uri': 'uri'})

    expected_query = "http://localhost:5005/Antho Room/spotify/queue/uri"

    actual_query = music_playback_service._generate_queue_query(track)

    assert expected_query == actual_query
    music_playback_service._generate_queue_query(track)


def test_generate_correct_url_query_for_clear_queue(connected_device, node_configuration):
    music_playback_service = SpotifyNodeMusicPlaybackService(connected_device, CONFIGURATION=node_configuration)

    expected_query = "http://localhost:5005/Antho Room/clearqueue"

    actual_query = music_playback_service._generate_clear_queue_query()

    assert expected_query == actual_query


@mock.patch('snipssonos.services.spotify.music_playback_service.FuturesSession.get')
def test_calls_queue(mocked_future, connected_device, node_configuration):
    music_playback_service = SpotifyNodeMusicPlaybackService(device=connected_device, CONFIGURATION=node_configuration)

    tracks = [Track.from_dict({'uri': 'uri{}'.format(str(i))}) for i in range(10)]
    music_playback_service.queue(connected_device, tracks)

    assert mocked_future.call_count == len(tracks)
