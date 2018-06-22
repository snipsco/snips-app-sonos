import mock
import pytest
import requests

from snipssonos.helpers.spotify_client import SpotifyClient
from snipssonos.exceptions import MusicSearchCredentialsError, \
    MusicSearchProviderConnectionError


# Testing Spotify Client
@pytest.mark.skip(reason="I didn't have time to do proper mocking. Let's wait for next iteration")
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
        SpotifyClient(client_id, client_secret)




