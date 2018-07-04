from snipssonos.services.node.query_builder import NodeQueryBuilder

BASE_ENDPOINT = "http://localhost:5005"


def test_query_is_generated_correctly():
    query_builder = NodeQueryBuilder("device_name", "deezer")

    query_builder.add_album_result_type()\
        .add_album_filter("my favourite album")

    query = query_builder.generate_search_query()
    expected_query = "{}/device_name/musicsearch/deezer/album/my favourite album".format(BASE_ENDPOINT)

    assert query == expected_query
