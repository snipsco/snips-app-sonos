import mock
import pytest
import requests

from snipssonos.services.spotify_music_search_service import SpotifyClient, SpotifyMusicSearchService, SpotifyAPIQueryBuilder
from snipssonos.exceptions import MusicSearchCredentialsError, MusicSearchProviderConnectionError


# Testing Music Search Service
def test_music_service_empty_song_name():
    pass


def test_music_service_song_name():
    pass



# Testing Spotify Client
@mock.patch('snipssonos.services.spotify_music_search_service.requests')
def test_spotify_client_raises_exception_connection_error(mocked_requests):
    mocked_requests.post.side_effect = requests.exceptions.ConnectionError

    client_id = "client_id"
    client_secret = "client_secret"

    client = SpotifyClient(client_id, client_secret)
    with pytest.raises(MusicSearchProviderConnectionError):
        client.retrieve_access_token()


def test_spotify_client_encodes_base_64_credentials():
    client_id = "client_id"
    client_secret = "client_secret"
    expected_base64_encoded_credentials = "Y2xpZW50X2lkOmNsaWVudF9zZWNyZXQ="
    client = SpotifyClient(client_id, client_secret)
    actual_base64_encoded_credentials = client._get_base_64_encoded_credentials()

    assert actual_base64_encoded_credentials == expected_base64_encoded_credentials


def test_spotify_client_encodes_base_64_raises_exception_with_empty_credentials():
    client_id = ""
    client_secret = "client_secret"

    with pytest.raises(MusicSearchCredentialsError):
        client = SpotifyClient(client_id, client_secret)


# Testing Spotify API Query Builder
def test_spotify_api_query_builder_add_search_term():
    qb = SpotifyAPIQueryBuilder()
    qb.add_search_term('roadhouse blues')

    actual_dict = qb.to_dict()

    expected_dict = {'q': 'roadhouse blues'}
    assert actual_dict['q'] == expected_dict['q']


def test_spotify_api_query_builder_add_field_filter():
    qb = SpotifyAPIQueryBuilder()
    qb.add_search_term('roadhouse blues')
    qb.add_field_filter('artist','antho')
    qb.add_field_filter('album', 'this is an album')

    actual_dict = qb.to_dict()

    expected_dict = {'q': 'artist:antho album:this is an album'}
    assert actual_dict['q'] == expected_dict['q']


def test_spotify_api_query_builder_add_result_type():
    qb = SpotifyAPIQueryBuilder()
    qb.add_search_term('roadhouse blues')
    qb.add_result_type('track')

    actual_dict = qb.to_dict()

    expected_dict = {'q': 'roadhouse blues', 'type': 'track'}
    assert actual_dict['q'] == expected_dict['q']
    assert actual_dict['type'] == expected_dict['type']
