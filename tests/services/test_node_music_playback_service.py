import mock
import pytest

from snipssonos.entities.device import Device
from snipssonos.entities.track import Track
from snipssonos.services.node_music_playback_service import NodeMusicPlaybackService


@pytest.fixture
def connected_device():
    return Device.from_dict({
        'identifier': 'RINCON_7828CA10127001400',
        'name': 'Antho Room',
        'volume': 18
    })


def test_music_playback_service_initialization(connected_device):
    music_playback_service = NodeMusicPlaybackService(connected_device)

    assert music_playback_service.PORT == NodeMusicPlaybackService.PORT
    assert music_playback_service.HOST == NodeMusicPlaybackService.HOST
    assert music_playback_service.PROTOCOL == NodeMusicPlaybackService.PROTOCOL


def test_generate_correct_url_query_for_get_method(connected_device):
    music_playback_service = NodeMusicPlaybackService(connected_device)

    track = Track.from_dict({'uri': 'uri'})

    expected_query = "http://localhost:5005/Antho Room/spotify/now/uri"

    actual_query = music_playback_service._generate_play_now_query(track)

    assert expected_query == actual_query

def test_generate_correct_url_query_for_queue(connected_device):
    music_playback_service = NodeMusicPlaybackService(connected_device)

    track = Track.from_dict({'uri': 'uri'})

    expected_query = "http://localhost:5005/Antho Room/spotify/queue/uri"

    actual_query = music_playback_service._generate_queue_query(track)

    assert expected_query == actual_query
    music_playback_service._generate_queue_query(track)

@mock.patch('snipssonos.services.node_music_playback_service.requests')
def test_calls_queue(mocked_request, connected_device):
    music_playback_service = NodeMusicPlaybackService(connected_device)

    tracks = [Track.from_dict({'uri':'uri{}'.format(str(i))})for i in range(10)]
    music_playback_service.queue(connected_device, tracks)

    assert mocked_request.get.call_count == len(tracks)