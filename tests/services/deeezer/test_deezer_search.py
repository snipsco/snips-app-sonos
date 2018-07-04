import mock, pytest
from snipssonos.services.deezer.music_search_and_play_service import DeezerMusicSearchService
from snipssonos.exceptions import MusicSearchProviderConnectionError

BASE_ENDPOINT = "http://localhost:5005"
DEVICE_NAME = "a_device"

@pytest.fixture
def deezer_search():
    deezer = DeezerMusicSearchService()
    device_name = DEVICE_NAME
    deezer.set_node_query_builder(device_name)
    return deezer


# check if the execution happened with the expected query
@mock.patch('snipssonos.services.deezer.music_search_and_play_service.NodeQueryBuilder')
def test_correctly_sets_node_query_builder(node_query_builder):
    deezer = DeezerMusicSearchService()
    deezer.set_node_query_builder("a_device")

    node_query_builder.assert_called_with("a_device", "deezer")


def test_proper_music_service_is_set():
    deezer = DeezerMusicSearchService()

    assert "deezer" == deezer.SERVICE_NAME


@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests.Response')
@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests')
def test_search_album(mock_requests, mock_response, deezer_search):
    deezer_search.search_album("favourite album")
    expected_query = "{}/{}/musicsearch/{}/{}/{}".format(BASE_ENDPOINT, DEVICE_NAME, "deezer",
                                                         "album", "favourite album")
    mock_response.ok.return_value = True
    mock_requests.get.return_value = mock_response
    mock_requests.get.assert_called_with(expected_query)


@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests.Response')
@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests')
def test_search_album_for_artist(mock_requests, mock_response, deezer_search):
    deezer_search.search_album_for_artist("favourite album", "favourite artist")
    expected_query = "{}/{}/musicsearch/{}/{}/{}".format(BASE_ENDPOINT, DEVICE_NAME, "deezer",
                                                         "album", "favourite album favourite artist")
    mock_response.ok.return_value = True
    mock_requests.get.return_value = mock_response
    mock_requests.get.assert_called_with(expected_query)


@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests.Response')
@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests')
def test_search_album_in_playlist(mock_requests, mock_response, deezer_search):
    deezer_search.search_album_in_playlist("favourite album", "vibing")
    expected_query = "{}/{}/musicsearch/{}/{}/{}".format(BASE_ENDPOINT, DEVICE_NAME, "deezer",
                                                         "album", "favourite album")
    mock_response.ok.return_value = True
    mock_requests.get.return_value = mock_response
    mock_requests.get.assert_called_with(expected_query)


@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests.Response')
@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests')
def test_search_album_for_artist_and_for_playlist(mock_requests, mock_response, deezer_search):
    deezer_search.search_album_for_artist_and_for_playlist("favourite album", "favourite artist", "balling")
    expected_query = "{}/{}/musicsearch/{}/{}/{}".format(BASE_ENDPOINT, DEVICE_NAME, "deezer",
                                                         "album", "favourite album favourite artist")
    mock_response.ok.return_value = True
    mock_requests.get.return_value = mock_response
    mock_requests.get.assert_called_with(expected_query)


@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests.Response')
@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests')
def test_search_track(mock_requests, mock_response, deezer_search):
    deezer_search.search_track("my fav track")

    expected_query = "{}/{}/musicsearch/{}/{}/{}".format(BASE_ENDPOINT, DEVICE_NAME, "deezer",
                                                         "song", "my fav track")
    mock_response.ok.return_value = True
    mock_requests.get.return_value = mock_response
    mock_requests.get.assert_called_with(expected_query)



@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests.Response')
@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests')
def test_search_track_for_artist(mock_requests, mock_response, deezer_search):
    deezer_search.search_track_for_artist("my fav track", "my fav artist")

    expected_query = "{}/{}/musicsearch/{}/{}/{}".format(BASE_ENDPOINT, DEVICE_NAME, "deezer",
                                                         "song", "my fav track my fav artist")
    mock_response.ok.return_value = True
    mock_requests.get.return_value = mock_response
    mock_requests.get.assert_called_with(expected_query)


@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests.Response')
@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests')
def test_search_track_for_album(mock_requests, mock_response, deezer_search):
    deezer_search.search_track_for_album("my fav track", "a very good album")

    expected_query = "{}/{}/musicsearch/{}/{}/{}".format(BASE_ENDPOINT, DEVICE_NAME, "deezer",
                                                         "song", "my fav track")
    mock_response.ok.return_value = True
    mock_requests.get.return_value = mock_response
    mock_requests.get.assert_called_with(expected_query)


@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests.Response')
@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests')
def test_search_track_for_playlist(mock_requests, mock_response, deezer_search):
    deezer_search.search_track_for_playlist("my fav track", "a very good playlist")

    expected_query = "{}/{}/musicsearch/{}/{}/{}".format(BASE_ENDPOINT, DEVICE_NAME, "deezer",
                                                         "song", "my fav track")
    mock_response.ok.return_value = True
    mock_requests.get.return_value = mock_response
    mock_requests.get.assert_called_with(expected_query)


@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests.Response')
@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests')
def search_track_for_album_and_for_artist(mock_requests, mock_response, deezer_search):
    deezer_search.search_track_for_album_and_for_artist("my fav track", "a very good album", "my fav artist")

    expected_query = "{}/{}/musicsearch/{}/{}/{}".format(BASE_ENDPOINT, DEVICE_NAME, "deezer",
                                                         "song", "my fav track my fav artist")
    mock_response.ok.return_value = True
    mock_requests.get.return_value = mock_response
    mock_requests.get.assert_called_with(expected_query)


@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests.Response')
@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests')
def search_track_for_album_and_for_playlist(mock_requests, mock_response, deezer_search):
    deezer_search.search_track_for_album_and_for_playlist("my fav track", "a very good album", "good vibes")

    expected_query = "{}/{}/musicsearch/{}/{}/{}".format(BASE_ENDPOINT, DEVICE_NAME, "deezer",
                                                         "song", "my fav track")
    mock_response.ok.return_value = True
    mock_requests.get.return_value = mock_response
    mock_requests.get.assert_called_with(expected_query)


@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests.Response')
@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests')
def search_track_for_album_and_for_playlist(mock_requests, mock_response, deezer_search):
    deezer_search.search_track_for_artist_and_for_playlist("my fav track", "a very good artist", "good vibes")

    expected_query = "{}/{}/musicsearch/{}/{}/{}".format(BASE_ENDPOINT, DEVICE_NAME, "deezer",
                                                         "song", "my fav track a very good artist")
    mock_response.ok.return_value = True
    mock_requests.get.return_value = mock_response
    mock_requests.get.assert_called_with(expected_query)


@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests.Response')
@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests')
def search_track_for_album_and_for_artist_and_for_playlist(mock_requests, mock_response, deezer_search):
    deezer_search.search_track_for_artist_and_for_playlist("my fav track", "a nice album", "a very good artist", "good vibes")

    expected_query = "{}/{}/musicsearch/{}/{}/{}".format(BASE_ENDPOINT, DEVICE_NAME, "deezer",
                                                         "song", "my fav track a very good artist")
    mock_response.ok.return_value = True
    mock_requests.get.return_value = mock_response
    mock_requests.get.assert_called_with(expected_query)


@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests.Response')
@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests')
def test_search_artist_for_playlist(mock_requests, mock_response, deezer_search):
    deezer_search.search_artist_for_playlist("my fav artist", "a playlist a used to like")

    expected_query = "{}/{}/musicsearch/{}/{}/{}".format(BASE_ENDPOINT, DEVICE_NAME, "deezer",
                                                         "song", "my fav artist")
    mock_response.ok.return_value = True
    mock_requests.get.return_value = mock_response
    mock_requests.get.assert_called_with(expected_query)


@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests.Response')
@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests')
def test_search_playlist(mock_requests, mock_response, deezer_search):
    deezer_search.search_playlist("good vibesssss")

    expected_query = "{}/{}/musicsearch/{}/{}/{}".format(BASE_ENDPOINT, DEVICE_NAME, "deezer",
                                                         "playlist", "good vibesssss")
    mock_response.ok.return_value = True
    mock_requests.get.return_value = mock_response
    mock_requests.get.assert_called_with(expected_query)


@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests.Response')
@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests')
def test_error_raised_on_request(mock_requests, mock_response, deezer_search):
    mock_response.ok.return_value = False
    mock_requests.get.return_value = mock_response

    with pytest.raises(MusicSearchProviderConnectionError):
        deezer_search.search_playlist("good vibesssss")










