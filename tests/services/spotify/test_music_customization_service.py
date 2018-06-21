import mock

from snipssonos.services.spotify.music_customization_service import SpotifyCustomizationService
from tests.services.spotify.raw_responses import TOP_ARTISTS, EMPTY_ITEMS, TOP_TRACKS

ENTITY_TYPES = ["artists", "tracks", "playlists"]


def test_music_customization_spotify_parse_artist_results():
    customization_service = SpotifyCustomizationService("client_id", "client_secret")
    artists = customization_service.parse_results("artists", TOP_ARTISTS)

    assert len(artists) == 20
    assert artists[0].name == "The Weeknd"
    assert artists[0].uri == "spotify:artist:1Xyo4u8uXC1ZmMpatF05PJ"


def test_music_customization_spotify_parse_track_results():
    customization_service = SpotifyCustomizationService("client_id", "client_secret")
    artists = customization_service.parse_results("tracks", TOP_TRACKS)

    assert len(artists) == 2
    assert artists[0].name == "I Feel It Coming"
    assert artists[0].uri == "spotify:track:4RepvCWqsP6zBuzvwYibAS"


def test_music_customization_correct_parsing_of_entities_with_empty_response():
    customization_service = SpotifyCustomizationService("client_id", "client_secret")
    tracks = customization_service.parse_results("artists", EMPTY_ITEMS)

    assert len(tracks) == 0


@mock.patch('snipssonos.services.spotify.music_customization_service.SpotifyClient')
def test_music_customization_fetch_top_artists(mock_spotify_client):
    mock_spotify_client_instance = mock_spotify_client.return_value
    mock_spotify_client_instance.execute_query.return_value = TOP_ARTISTS

    customization_service = SpotifyCustomizationService("client_id", "client_secret")
    artists = customization_service.fetch_entity("artists")

    assert len(artists) == 60
    assert artists[0].name == "The Weeknd"
    assert artists[0].uri == "spotify:artist:1Xyo4u8uXC1ZmMpatF05PJ"
    
    
@mock.patch('snipssonos.services.spotify.music_customization_service.SpotifyClient')
def test_music_customization_fetch_top_tracks(mock_spotify_client):
    mock_spotify_client_instance = mock_spotify_client.return_value
    mock_spotify_client_instance.execute_query.return_value = TOP_TRACKS

    customization_service = SpotifyCustomizationService("client_id", "client_secret")
    artists = customization_service.fetch_entity("tracks")

    assert len(artists) == 6
    assert artists[0].name == "I Feel It Coming"
    assert artists[0].uri == "spotify:track:4RepvCWqsP6zBuzvwYibAS"

