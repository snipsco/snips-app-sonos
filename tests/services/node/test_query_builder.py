#coding: utf-8
import pytest

from snipssonos.exceptions import NodeQueryBuilderUnavailableMusicService, NodeQueryBuilderMissingQueryData
from snipssonos.services.node.query_builder import NodeQueryBuilder

BASE_ENDPOINT = "http://localhost:5005"


@pytest.fixture
def query_builder():
    return NodeQueryBuilder("device_name", "deezer")


def test_set_music_service(query_builder):
    query_builder.set_music_service("spotify")

    assert "spotify" == query_builder.music_service


def test_set_unavailable_music_service(query_builder):
    with pytest.raises(NodeQueryBuilderUnavailableMusicService):
        query_builder.set_music_service("blablabla")


def test_add_result_type(query_builder):
    query_builder.add_result_type("my_type")

    assert query_builder.result_type == "my_type"


def test_add_track_result_type(query_builder):
    query_builder.add_track_result_type()

    assert query_builder.result_type == "song"


def test_add_album_result_type(query_builder):
    query_builder.add_album_result_type()

    assert query_builder.result_type == "album"


def test_add_playlist_result_type(query_builder):
    query_builder.add_playlist_result_type()

    assert query_builder.result_type == "playlist"


def test_add_track_filter(query_builder):
    query_builder.add_track_filter("HUMBLE")

    assert "HUMBLE" in [filter_value for (filter_type, filter_value) in query_builder.field_filters]


def test_add_artist_filter(query_builder):
    query_builder.add_artist_filter("Madonna")

    assert "Madonna" in [filter_value for (filter_type, filter_value) in query_builder.field_filters]


def test_add_album_filter(query_builder):
    query_builder.add_album_filter("Scorpion")

    assert "Scorpion" in [filter_value for (filter_type, filter_value) in query_builder.field_filters]


def test_add_playlist_filter(query_builder):
    query_builder.add_playlist_filter("Summer Vibes")

    assert "Summer Vibes" in [filter_value for (filter_type, filter_value) in query_builder.field_filters]


def test_composition_of_filters(query_builder):
    query_builder \
        .add_playlist_filter("Summer Vibes") \
        .add_artist_filter("Madonna")

    field_filters_values = [filter_value for (filter_type, filter_value) in query_builder.field_filters]
    assert "Summer Vibes" in field_filters_values and "Madonna" in field_filters_values


def test_query_is_generated_correctly(query_builder):
    query_builder.add_album_result_type() \
        .add_album_filter("my favourite album")

    query = query_builder.generate_search_query()
    expected_query = '{}/device_name/musicsearch/deezer/album/my favourite album'.format(BASE_ENDPOINT)

    assert query == expected_query


def test_query_is_generated_correctly_when_combining_two_field_filters(query_builder):
    query_builder.add_album_result_type() \
        .add_artist_filter("Nina Simone") \
        .add_album_filter("Feeling Good")

    query = query_builder.generate_search_query()
    expected_query = '{}/device_name/musicsearch/deezer/album/artist:"Nina Simone":album:"Feeling Good"'.format(
        BASE_ENDPOINT)

    assert query == expected_query


def test_query_is_generated_correctly_when_combining_three_field_filters(query_builder):
    query_builder.add_album_result_type() \
        .add_artist_filter("Nina Simone") \
        .add_album_filter("Feeling Good") \
        .add_track_filter("My Baby Just Cares For Me")

    query = query_builder.generate_search_query()
    expected_query = '{}/device_name/musicsearch/deezer/album/artist:"Nina Simone":album:"Feeling Good":track:"My Baby Just Cares For Me"'.format(
        BASE_ENDPOINT)

    assert query == expected_query


def test_query_is_invalid_with_empty_field_filter(query_builder):
    with pytest.raises(NodeQueryBuilderMissingQueryData) as e:
        query_builder.add_album_result_type() \
            .add_artist_filter("")


def test_query_is_invalid_with_none_field_filter(query_builder):
    with pytest.raises(NodeQueryBuilderMissingQueryData) as e:
        query_builder.add_album_result_type() \
            .add_album_filter(None)


@pytest.mark.skip("Encoding errors")
def test_query_is_valid_with_special_characters(query_builder):
    query_builder.add_album_result_type() \
        .add_artist_filter("Beyoncé") \
        .add_album_filter("I AM .. SASHA FIERCE")

    query = query_builder.generate_search_query()

    expected_query = '{}/device_name/musicsearch/deezer/album/artist:"Beyoncé":album:"I AM .. SASHA FIERCE"'.format(BASE_ENDPOINT)
    assert query == expected_query
    assert type(query) == unicode
