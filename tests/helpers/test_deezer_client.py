import pytest

from snipssonos.exceptions import MusicSearchCredentialsError
from snipssonos.helpers.deezer_client import DeezerClient

MOCK_APP_ID = "1234567890"
MOCK_APP_SECRET = "A1Z2E3R4T5Y6U7I8O9P0"


def test_check_credentials_validity():
    with pytest.raises(MusicSearchCredentialsError):
        dz = DeezerClient("", MOCK_APP_SECRET)


def test_access_token_extraction():
    dz = DeezerClient(MOCK_APP_ID, MOCK_APP_SECRET)
    expected_access_token = "A1Z2E3R4FFGO09I8U7Y6T5REZ2"
    text_response = "access_token={}&expires=234567890987".format(expected_access_token)

    extracted_token = dz._extract_access_token(text_response)
    assert extracted_token == expected_access_token


def test_expires_in_extraction():
    dz = DeezerClient(MOCK_APP_ID, MOCK_APP_SECRET)
    expected_access_token = "A1Z2E3R4FFGO09I8U7Y6T5REZ2"
    expires_in = 3600
    text_response = "access_token={}&expires={}".format(expected_access_token, expires_in)

    extracted_expires_in = dz._extract_access_token_expiration(text_response)
    assert extracted_expires_in == expires_in