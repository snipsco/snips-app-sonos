import pytest

from snipssonos.helpers.spotify_client import SpotifyAPISearchQueryBuilder
from snipssonos.exceptions import SpotifyQueryBuilderNonExistentTimeRange,\
    SpotifyQueryBuilderUserDataQueryNotSet

# Testing Spotify API Search Query Builder
def test_spotify_api_query_builder_add_search_term():
    qb = SpotifyAPISearchQueryBuilder()
    qb.add_generic_search_term('roadhouse blues')

    actual_dict = qb.to_dict()

    expected_dict = {'q': 'roadhouse blues'}
    assert actual_dict['q'] == expected_dict['q']


def test_spotify_api_query_builder_add_field_filter():
    qb = SpotifyAPISearchQueryBuilder()
    qb.add_generic_search_term('roadhouse blues')
    qb.add_field_filter('artist', 'antho')
    qb.add_field_filter('album', 'this is an album')

    actual_dict = qb.to_dict()

    expected_dict = {'q': 'artist:antho album:this is an album'}
    assert actual_dict['q'] == expected_dict['q']


def test_spotify_api_query_builder_add_result_type():
    qb = SpotifyAPISearchQueryBuilder()
    qb.add_generic_search_term('roadhouse blues')
    qb.add_result_type('track')

    actual_dict = qb.to_dict()

    expected_dict = {'q': 'roadhouse blues', 'type': 'track'}
    assert actual_dict['q'] == expected_dict['q']
    assert actual_dict['type'] == expected_dict['type']


def test_spotify_api_query_builder_add_track_result_type():
    qb = SpotifyAPISearchQueryBuilder()
    qb.add_generic_search_term('roadhouse blues')
    qb.add_track_result_type()

    actual_dict = qb.to_dict()

    expected_dict = {'q': 'roadhouse blues', 'type': 'track'}
    assert actual_dict['q'] == expected_dict['q']
    assert actual_dict['type'] == expected_dict['type']


def test_spotify_api_query_builder_add_album_result_type():
    qb = SpotifyAPISearchQueryBuilder()
    qb.add_generic_search_term('roadhouse blues')
    qb.add_album_result_type()

    actual_dict = qb.to_dict()

    expected_dict = {'q': 'roadhouse blues', 'type': 'album'}
    assert actual_dict['q'] == expected_dict['q']
    assert actual_dict['type'] == expected_dict['type']


def test_spotify_api_query_builder_add_artist_result_type():
    qb = SpotifyAPISearchQueryBuilder()
    qb.add_generic_search_term('roadhouse blues')
    qb.add_artist_result_type()

    actual_dict = qb.to_dict()

    expected_dict = {'q': 'roadhouse blues', 'type': 'artist'}
    assert actual_dict['q'] == expected_dict['q']
    assert actual_dict['type'] == expected_dict['type']


def test_spotify_api_query_builder_add_playlist_result_type():
    qb = SpotifyAPISearchQueryBuilder()
    qb.add_generic_search_term('roadhouse blues')
    qb.add_playlist_result_type()

    actual_dict = qb.to_dict()

    expected_dict = {'q': 'roadhouse blues', 'type': 'playlist'}
    assert actual_dict['q'] == expected_dict['q']
    assert actual_dict['type'] == expected_dict['type']


def test_spotify_api_query_builder_add_artist_filter():
    qb = SpotifyAPISearchQueryBuilder()
    qb.add_generic_search_term('roadhouse blues')
    qb.add_artist_filter("antho")

    actual_query_dict = qb.to_dict()

    expected_query_dict = {'q': 'artist:antho'}
    assert actual_query_dict['q'] == expected_query_dict['q']


def test_spotify_api_query_builder_add_track_filter():
    qb = SpotifyAPISearchQueryBuilder()
    qb.add_generic_search_term('roadhouse blues')
    qb.add_track_filter("pernety")

    actual_query_dict = qb.to_dict()

    expected_query_dict = {'q': 'track:pernety'}
    assert actual_query_dict['q'] == expected_query_dict['q']


def test_spotify_api_query_builder_add_time_range():
    qb = SpotifyAPISearchQueryBuilder(True).add_time_range('long_term')
    actual_query_dict = qb.to_dict()
    expected_query_dict = {'time_range': 'long_term'}
    assert actual_query_dict['time_range'] == expected_query_dict['time_range']


def test_spotify_api_query_builder_add_limit():
    qb = SpotifyAPISearchQueryBuilder(True).add_limit(20)
    actual_query_dict = qb.to_dict()
    expected_query_dict = {'limit': 20}
    assert actual_query_dict['limit'] == expected_query_dict['limit']


def test_spotify_api_query_builder_add_time_range_raises_exception():
    with pytest.raises(SpotifyQueryBuilderNonExistentTimeRange):
        SpotifyAPISearchQueryBuilder(True).add_time_range('I_do_not_exist')


def test_spotify_api_query_builder_add_time_range_when_request_user_data_not_set_raises_exception():
    with pytest.raises(SpotifyQueryBuilderUserDataQueryNotSet):
        SpotifyAPISearchQueryBuilder().add_time_range('long_term')


