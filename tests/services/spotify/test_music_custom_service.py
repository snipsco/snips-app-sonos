import mock

from snipssonos.services.spotify.music_custom_service import SpotifyCustomService
from tests.services.spotify.raw_responses import TOP_ARTISTS, EMPTY_ITEMS


def test_spotify_parse_artist_results():
    client = SpotifyCustomService("client_id", "client_secret")
    artists = client.parse_artist_results(TOP_ARTISTS)

    assert len(artists) == 20
    assert artists[0].name == "The Weeknd"
    assert artists[0].uri == "spotify:artist:1Xyo4u8uXC1ZmMpatF05PJ"


def test_correct_parsing_of_tracks_with_empty_response():
    client = SpotifyCustomService("client_id", "client_secret")
    tracks = client.parse_artist_results(EMPTY_ITEMS)

    assert len(tracks) == 0

@mock.patch('snipssonos.services.spotify.music_custom_service.SpotifyClient')
def test_fetch_top_artists(mock_spotify_client):
    mock_spotify_client_instance = mock_spotify_client.return_value
    mock_spotify_client_instance.execute_query.return_value = TOP_ARTISTS

    client = SpotifyCustomService("client_id", "client_secret")
    artists = client.fetch_top_artist()

    assert len(artists) == 60
    assert artists[0].name == "The Weeknd"
    assert artists[0].uri == "spotify:artist:1Xyo4u8uXC1ZmMpatF05PJ"

