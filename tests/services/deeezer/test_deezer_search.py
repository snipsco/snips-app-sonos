import mock, pytest

from snipssonos.entities.device import Device
from snipssonos.services.deezer.music_search_and_play_service import DeezerMusicSearchService
from snipssonos.services.node.query_builder import NodeQueryBuilder
from snipssonos.exceptions import MusicSearchProviderConnectionError

BASE_ENDPOINT = "http://localhost:5005"


@pytest.fixture
def connected_device():
    return Device(
        name="Anthony's Sonos",
        identifier="RINCON_XXXX",
        volume=10
    )


@pytest.fixture
def deezer_music_search_service():

    connected_device = Device(
        name="Anthony's Sonos",
        identifier="RINCON_XXXX",
        volume=10
    )

    mock_device_discovery_service = mock.Mock()
    mock_device_discovery_service.get.return_value = connected_device
    deezer = DeezerMusicSearchService(mock_device_discovery_service)
    return deezer


@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests.Response')
@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests')
def test_search_album(mock_requests, mock_response, deezer_music_search_service,
                      connected_device):

    # This test is dumb, it mocks stuff after they are supposed to be called ...

    deezer_music_search_service.search_album("favourite album")
    expected_query = "{}/{}/musicsearch/{}/{}/{}".format(BASE_ENDPOINT, connected_device.name, "deezer",
                                                         "album", "favourite album")
    mock_requests.get.assert_called_with(expected_query)


@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests.Response')
@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests')
def test_search_album_for_artist(mock_requests, mock_response, deezer_music_search_service, connected_device):
    deezer_music_search_service.search_album_for_artist("favourite album", "favourite artist")

    expected_query = "{}/{}/musicsearch/{}/{}/{}".format(BASE_ENDPOINT, connected_device.name, "deezer",
                                                         "album", "favourite album favourite artist")

    mock_requests.get.assert_called_with(expected_query)


@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests.Response')
@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests')
def test_search_album_in_playlist(mock_requests, mock_response, deezer_music_search_service, connected_device):
    deezer_music_search_service.search_album_in_playlist("favourite album", "vibing")
    expected_query = "{}/{}/musicsearch/{}/{}/{}".format(BASE_ENDPOINT, connected_device.name, "deezer",
                                                         "album", "favourite album")

    mock_requests.get.assert_called_with(expected_query)


@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests.Response')
@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests')
def test_search_album_for_artist_and_for_playlist(mock_requests, mock_response, deezer_music_search_service,
                                                  connected_device):
    deezer_music_search_service.search_album_for_artist_and_for_playlist("favourite album", "favourite artist",
                                                                         "balling")
    expected_query = "{}/{}/musicsearch/{}/{}/{}".format(BASE_ENDPOINT, connected_device.name, "deezer",
                                                         "album", "favourite album favourite artist")

    mock_requests.get.assert_called_with(expected_query)


@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests.Response')
@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests')
def test_search_track(mock_requests, mock_response, deezer_music_search_service, connected_device):
    deezer_music_search_service.search_track("my fav track")

    expected_query = "{}/{}/musicsearch/{}/{}/{}".format(BASE_ENDPOINT, connected_device.name, "deezer",
                                                         "song", "my fav track")
    mock_requests.get.assert_called_with(expected_query)


@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests.Response')
@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests')
def test_search_track_for_artist(mock_requests, mock_response, deezer_music_search_service, connected_device):
    deezer_music_search_service.search_track_for_artist("my fav track", "my fav artist")

    expected_query = "{}/{}/musicsearch/{}/{}/{}".format(BASE_ENDPOINT, connected_device.name, "deezer",
                                                         "song", "my fav track my fav artist")
    mock_requests.get.assert_called_with(expected_query)


@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests.Response')
@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests')
def test_search_track_for_album(mock_requests, mock_response, deezer_music_search_service, connected_device):
    deezer_music_search_service.search_track_for_album("my fav track", "a very good album")

    expected_query = "{}/{}/musicsearch/{}/{}/{}".format(BASE_ENDPOINT, connected_device.name, "deezer",
                                                         "song", "my fav track")
    mock_requests.get.assert_called_with(expected_query)


@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests.Response')
@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests')
def test_search_track_for_playlist(mock_requests, mock_response, deezer_music_search_service, connected_device):
    deezer_music_search_service.search_track_for_playlist("my fav track", "a very good playlist")

    expected_query = "{}/{}/musicsearch/{}/{}/{}".format(BASE_ENDPOINT, connected_device.name, "deezer",
                                                         "song", "my fav track")
    mock_requests.get.assert_called_with(expected_query)


@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests.Response')
@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests')
def search_track_for_album_and_for_artist(mock_requests, mock_response, deezer_music_search_service, connected_device):
    deezer_music_search_service.search_track_for_album_and_for_artist("my fav track", "a very good album",
                                                                      "my fav artist")

    expected_query = "{}/{}/musicsearch/{}/{}/{}".format(BASE_ENDPOINT, connected_device.name, "deezer",
                                                         "song", "my fav track my fav artist")
    mock_requests.get.assert_called_with(expected_query)


@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests.Response')
@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests')
def search_track_for_album_and_for_playlist(mock_requests, mock_response, deezer_music_search_service,
                                            connected_device):
    deezer_music_search_service.search_track_for_album_and_for_playlist("my fav track", "a very good album",
                                                                        "good vibes")

    expected_query = "{}/{}/musicsearch/{}/{}/{}".format(BASE_ENDPOINT, connected_device.name, "deezer",
                                                         "song", "my fav track")
    mock_requests.get.assert_called_with(expected_query)


@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests.Response')
@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests')
def search_track_for_album_and_for_playlist(mock_requests, mock_response, deezer_music_search_service,
                                            connected_device):
    deezer_music_search_service.search_track_for_artist_and_for_playlist("my fav track", "a very good artist",
                                                                         "good vibes")

    expected_query = "{}/{}/musicsearch/{}/{}/{}".format(BASE_ENDPOINT, connected_device.name, "deezer",
                                                         "song", "my fav track a very good artist")
    mock_requests.get.assert_called_with(expected_query)


@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests.Response')
@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests')
def search_track_for_album_and_for_artist_and_for_playlist(mock_requests, mock_response, deezer_music_search_service,
                                                           connected_device):
    deezer_music_search_service.search_track_for_artist_and_for_playlist("my fav track", "a nice album",
                                                                         "a very good artist", "good vibes")

    expected_query = "{}/{}/musicsearch/{}/{}/{}".format(BASE_ENDPOINT, connected_device.name, "deezer",
                                                         "song", "my fav track a very good artist")
    mock_requests.get.assert_called_with(expected_query)


@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests.Response')
@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests')
def test_search_artist_for_playlist(mock_requests, mock_response, deezer_music_search_service, connected_device):
    deezer_music_search_service.search_artist_for_playlist("my fav artist", "a playlist a used to like")

    expected_query = "{}/{}/musicsearch/{}/{}/{}".format(BASE_ENDPOINT, connected_device.name, "deezer",
                                                         "song", "my fav artist")
    mock_requests.get.assert_called_with(expected_query)


@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests.Response')
@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests')
def test_search_playlist(mock_requests, mock_response, deezer_music_search_service, connected_device):
    deezer_music_search_service.search_playlist("good vibesssss")

    expected_query = "{}/{}/musicsearch/{}/{}/{}".format(BASE_ENDPOINT, connected_device.name, "deezer",
                                                         "playlist", "good vibesssss")
    mock_requests.get.assert_called_with(expected_query)


@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests.Response')
@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests')
def test_error_raised_on_request(mock_requests, mock_response, deezer_music_search_service, connected_device):
    mock_response.ok = False
    mock_requests.get.return_value = mock_response

    with pytest.raises(MusicSearchProviderConnectionError):
        deezer_music_search_service.search_playlist("good vibesssss")
