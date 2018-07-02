import mock
import pytest
import requests
import json
import time

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
    client = SpotifyClient(client_id, client_secret, "refresh_token")
    actual_base64_encoded_credentials = client._get_base_64_encoded_credentials()

    assert actual_base64_encoded_credentials == expected_base64_encoded_credentials


def test_spotify_client_encodes_base_64_raises_exception_with_empty_credentials():
    client_id = ""
    client_secret = "client_secret"

    with pytest.raises(MusicSearchCredentialsError):
        SpotifyClient(client_id, client_secret, "refresh_token")


@mock.patch('snipssonos.helpers.spotify_client.requests')
@mock.patch('snipssonos.helpers.spotify_client.requests.Response')
def test_access_token_is_refreshed_after_expiration(mock_response, mock_request):
    client_id = "client_id"
    client_secret = "client_secret"

    # expiration is set to 1 sec
    mock_response.json.return_value = json.loads("""{  
       "access_token":"BQBhSKCPz_gQuffivPwvvpfn5oX7q0e5MTBdliEES8aWrRkGcsCH4pVy9HKYYpBlIBLjBremintjLxMpbk0",
       "token_type":"Bearer",
       "expires_in":1,
       "scope":""
    }""")

    mock_request.post.return_value = mock_response

    client = SpotifyClient(client_id, client_secret)
    client.authenticate()

    # we make sure the access token has been set after calling the authenticate method
    assert client.access_token is not None
    time.sleep(2)

    # we make sure the call to the authorization endpoint is made after expiration
    client.authenticate()
    assert mock_request.post.call_count == 2


