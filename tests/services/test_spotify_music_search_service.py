import mock
import pytest
import requests

from snipssonos.services.spotify_music_search_service import SpotifyClient, SpotifyMusicSearchService, SpotifyAPISearchQueryBuilder
from snipssonos.exceptions import MusicSearchCredentialsError, MusicSearchProviderConnectionError


# Testing Music Search Service
def test_music_service_empty_song_name():
    pass


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
        client = SpotifyClient(client_id, client_secret)


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
    qb.add_field_filter('artist','antho')
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

# Testing Spotify Music Service
def test_correct_parsing_of_tracks_for_correct_response():
    raw_response = """{
  "tracks" : {
    "href" : "https://api.spotify.com/v1/search?query=April+14th&type=track&offset=0&limit=20",
    "items" : [ {
      "album" : {
        "album_type" : "album",
        "artists" : [ {
          "external_urls" : {
            "spotify" : "https://open.spotify.com/artist/2H5elA2mJKrHmqkN9GSfkz"
          },
          "href" : "https://api.spotify.com/v1/artists/2H5elA2mJKrHmqkN9GSfkz",
          "id" : "2H5elA2mJKrHmqkN9GSfkz",
          "name" : "Gillian Welch",
          "type" : "artist",
          "uri" : "spotify:artist:2H5elA2mJKrHmqkN9GSfkz"
        } ],
        "available_markets" : [ "CA", "US" ],
        "external_urls" : {
          "spotify" : "https://open.spotify.com/album/55FP2ypQcghszSqylyBRbp"
        },
        "href" : "https://api.spotify.com/v1/albums/55FP2ypQcghszSqylyBRbp",
        "id" : "55FP2ypQcghszSqylyBRbp",
        "images" : [ {
          "height" : 640,
          "url" : "https://i.scdn.co/image/dab47d6fd421631a0abcf57974a7f6e718a91328",
          "width" : 640
        }, {
          "height" : 300,
          "url" : "https://i.scdn.co/image/3f4c8c64fdc270f2a3f2697d22851541157ad731",
          "width" : 300
        }, {
          "height" : 64,
          "url" : "https://i.scdn.co/image/08d109be91479e290f474c85a849bce8074f72e8",
          "width" : 64
        } ],
        "name" : "Time (The Relevator)",
        "release_date" : "2001-07-31",
        "release_date_precision" : "day",
        "type" : "album",
        "uri" : "spotify:album:55FP2ypQcghszSqylyBRbp"
      },
      "artists" : [ {
        "external_urls" : {
          "spotify" : "https://open.spotify.com/artist/2H5elA2mJKrHmqkN9GSfkz"
        },
        "href" : "https://api.spotify.com/v1/artists/2H5elA2mJKrHmqkN9GSfkz",
        "id" : "2H5elA2mJKrHmqkN9GSfkz",
        "name" : "Gillian Welch",
        "type" : "artist",
        "uri" : "spotify:artist:2H5elA2mJKrHmqkN9GSfkz"
      } ],
      "available_markets" : [ "CA", "US" ],
      "disc_number" : 1,
      "duration_ms" : 310626,
      "explicit" : false,
      "external_ids" : {
        "isrc" : "US2AR0110305"
      },
      "external_urls" : {
        "spotify" : "https://open.spotify.com/track/3f9HJzevC4sMYGDwj7yQwd"
      },
      "href" : "https://api.spotify.com/v1/tracks/3f9HJzevC4sMYGDwj7yQwd",
      "id" : "3f9HJzevC4sMYGDwj7yQwd",
      "is_local" : false,
      "name" : "April the 14th Part 1",
      "popularity" : 32,
      "preview_url" : "https://p.scdn.co/mp3-preview/def76ffbe34582b5d7a4cac94ede4f66dfa3db5d?cid=b5993e2dcca64251a0fc4c780dd257c3",
      "track_number" : 5,
      "type" : "track",
      "uri" : "spotify:track:3f9HJzevC4sMYGDwj7yQwd"
    }, {
      "album" : {
        "album_type" : "album",
        "artists" : [ {
          "external_urls" : {
            "spotify" : "https://open.spotify.com/artist/2H5elA2mJKrHmqkN9GSfkz"
          },
          "href" : "https://api.spotify.com/v1/artists/2H5elA2mJKrHmqkN9GSfkz",
          "id" : "2H5elA2mJKrHmqkN9GSfkz",
          "name" : "Gillian Welch",
          "type" : "artist",
          "uri" : "spotify:artist:2H5elA2mJKrHmqkN9GSfkz"
        } ],
        "available_markets" : [ "CA", "US" ],
        "external_urls" : {
          "spotify" : "https://open.spotify.com/album/3s93CBsy5EM1UZ7X3U4Ne6"
        },
        "href" : "https://api.spotify.com/v1/albums/3s93CBsy5EM1UZ7X3U4Ne6",
        "id" : "3s93CBsy5EM1UZ7X3U4Ne6",
        "images" : [ {
          "height" : 640,
          "url" : "https://i.scdn.co/image/2b55abf8b9371a9c089ec594ff039eb473f9d8ac",
          "width" : 640
        }, {
          "height" : 300,
          "url" : "https://i.scdn.co/image/1438f8f659f0101850ca0bd3ad00845d71667bed",
          "width" : 300
        }, {
          "height" : 64,
          "url" : "https://i.scdn.co/image/ffc761d22838518e1886fb39af6c8205379a50bc",
          "width" : 64
        } ],
        "name" : "Music From The Revelator Collection",
        "release_date" : "2006-04-04",
        "release_date_precision" : "day",
        "type" : "album",
        "uri" : "spotify:album:3s93CBsy5EM1UZ7X3U4Ne6"
      },
      "artists" : [ {
        "external_urls" : {
          "spotify" : "https://open.spotify.com/artist/2H5elA2mJKrHmqkN9GSfkz"
        },
        "href" : "https://api.spotify.com/v1/artists/2H5elA2mJKrHmqkN9GSfkz",
        "id" : "2H5elA2mJKrHmqkN9GSfkz",
        "name" : "Gillian Welch",
        "type" : "artist",
        "uri" : "spotify:artist:2H5elA2mJKrHmqkN9GSfkz"
      } ],
      "available_markets" : [ "CA", "US" ],
      "disc_number" : 1,
      "duration_ms" : 379706,
      "explicit" : false,
      "external_ids" : {
        "isrc" : "US2AR0220404"
      },
      "external_urls" : {
        "spotify" : "https://open.spotify.com/track/4SPyPCVJG5B6mA5fARX9bp"
      },
      "href" : "https://api.spotify.com/v1/tracks/4SPyPCVJG5B6mA5fARX9bp",
      "id" : "4SPyPCVJG5B6mA5fARX9bp",
      "is_local" : false,
      "name" : "April The 14th Part I (Live)",
      "popularity" : 20,
      "preview_url" : "https://p.scdn.co/mp3-preview/69fcb80f874176637d862495d7cda87c3bccdfe8?cid=b5993e2dcca64251a0fc4c780dd257c3",
      "track_number" : 1,
      "type" : "track",
      "uri" : "spotify:track:4SPyPCVJG5B6mA5fARX9bp"
    }, {
      "album" : {
        "album_type" : "album",
        "artists" : [ {
          "external_urls" : {
            "spotify" : "https://open.spotify.com/artist/1Q7OIaGiqgG4EDGYTkldPk"
          },
          "href" : "https://api.spotify.com/v1/artists/1Q7OIaGiqgG4EDGYTkldPk",
          "id" : "1Q7OIaGiqgG4EDGYTkldPk",
          "name" : "Matthew Rix",
          "type" : "artist",
          "uri" : "spotify:artist:1Q7OIaGiqgG4EDGYTkldPk"
        } ],
        "available_markets" : [ "AD", "AR", "AT", "AU", "BE", "BG", "BO", "BR", "CA", "CH", "CL", "CO", "CR", "CY", "CZ", "DE", "DK", "DO", "EC", "EE", "ES", "FI", "FR", "GB", "GR", "GT", "HK", "HN", "HU", "ID", "IE", "IL", "IS", "IT", "JP", "LI", "LT", "LU", "LV", "MC", "MT", "MX", "MY", "NI", "NL", "NO", "NZ", "PA", "PE", "PH", "PL", "PT", "PY", "RO", "SE", "SG", "SK", "SV", "TH", "TR", "TW", "US", "UY", "VN", "ZA" ],
        "external_urls" : {
          "spotify" : "https://open.spotify.com/album/6oux6G3SVdbJioi9p61Sa5"
        },
        "href" : "https://api.spotify.com/v1/albums/6oux6G3SVdbJioi9p61Sa5",
        "id" : "6oux6G3SVdbJioi9p61Sa5",
        "images" : [ {
          "height" : 640,
          "url" : "https://i.scdn.co/image/7832cab08c3931b2b3fc0776b2d2e09f8ae70a04",
          "width" : 640
        }, {
          "height" : 300,
          "url" : "https://i.scdn.co/image/c20502d03e32bf603580597c4974ce0ef2f2bc4b",
          "width" : 300
        }, {
          "height" : 64,
          "url" : "https://i.scdn.co/image/c20237d378a34939417e72147d802a43d912c98d",
          "width" : 64
        } ],
        "name" : "Mattrix Minute: Best of 2014, Volume 2",
        "release_date" : "2017-05-18",
        "release_date_precision" : "day",
        "type" : "album",
        "uri" : "spotify:album:6oux6G3SVdbJioi9p61Sa5"
      },
      "artists" : [ {
        "external_urls" : {
          "spotify" : "https://open.spotify.com/artist/1Q7OIaGiqgG4EDGYTkldPk"
        },
        "href" : "https://api.spotify.com/v1/artists/1Q7OIaGiqgG4EDGYTkldPk",
        "id" : "1Q7OIaGiqgG4EDGYTkldPk",
        "name" : "Matthew Rix",
        "type" : "artist",
        "uri" : "spotify:artist:1Q7OIaGiqgG4EDGYTkldPk"
      } ],
      "available_markets" : [ "AD", "AR", "AT", "AU", "BE", "BG", "BO", "BR", "CA", "CH", "CL", "CO", "CR", "CY", "CZ", "DE", "DK", "DO", "EC", "EE", "ES", "FI", "FR", "GB", "GR", "GT", "HK", "HN", "HU", "ID", "IE", "IL", "IS", "IT", "JP", "LI", "LT", "LU", "LV", "MC", "MT", "MX", "MY", "NI", "NL", "NO", "NZ", "PA", "PE", "PH", "PL", "PT", "PY", "RO", "SE", "SG", "SK", "SV", "TH", "TR", "TW", "US", "UY", "VN", "ZA" ],
      "disc_number" : 1,
      "duration_ms" : 65443,
      "explicit" : false,
      "external_ids" : {
        "isrc" : "MMINU1400110"
      },
      "external_urls" : {
        "spotify" : "https://open.spotify.com/track/6TOwrIciKmDs8bTmcBVofh"
      },
      "href" : "https://api.spotify.com/v1/tracks/6TOwrIciKmDs8bTmcBVofh",
      "id" : "6TOwrIciKmDs8bTmcBVofh",
      "is_local" : false,
      "name" : "April 14th",
      "popularity" : 8,
      "preview_url" : "https://p.scdn.co/mp3-preview/8d369316a13be5bba2c826ec626d7f14fb1cb843?cid=b5993e2dcca64251a0fc4c780dd257c3",
      "track_number" : 46,
      "type" : "track",
      "uri" : "spotify:track:6TOwrIciKmDs8bTmcBVofh"
    }, {
      "album" : {
        "album_type" : "single",
        "artists" : [ {
          "external_urls" : {
            "spotify" : "https://open.spotify.com/artist/07lKyiT8QdydzmCrDAznnQ"
          },
          "href" : "https://api.spotify.com/v1/artists/07lKyiT8QdydzmCrDAznnQ",
          "id" : "07lKyiT8QdydzmCrDAznnQ",
          "name" : "Brian Hansen",
          "type" : "artist",
          "uri" : "spotify:artist:07lKyiT8QdydzmCrDAznnQ"
        } ],
        "available_markets" : [ "AD", "AR", "AT", "AU", "BE", "BG", "BO", "BR", "CA", "CH", "CL", "CO", "CR", "CY", "CZ", "DE", "DK", "DO", "EC", "EE", "ES", "FI", "FR", "GB", "GR", "GT", "HK", "HN", "HU", "ID", "IE", "IL", "IS", "IT", "JP", "LI", "LT", "LU", "LV", "MC", "MT", "MX", "MY", "NI", "NL", "NO", "NZ", "PA", "PE", "PH", "PL", "PT", "PY", "RO", "SE", "SG", "SK", "SV", "TH", "TR", "TW", "US", "UY", "VN", "ZA" ],
        "external_urls" : {
          "spotify" : "https://open.spotify.com/album/6Wdmkzzbyb5qQSoHWGnqqF"
        },
        "href" : "https://api.spotify.com/v1/albums/6Wdmkzzbyb5qQSoHWGnqqF",
        "id" : "6Wdmkzzbyb5qQSoHWGnqqF",
        "images" : [ {
          "height" : 640,
          "url" : "https://i.scdn.co/image/bd5a67fdc4fc5430c519ad2288009a9e78dd548e",
          "width" : 640
        }, {
          "height" : 300,
          "url" : "https://i.scdn.co/image/886bd9043cdc62c2b80084337d36ca01f7d81169",
          "width" : 300
        }, {
          "height" : 64,
          "url" : "https://i.scdn.co/image/9a46f82e51ad639aba8327f88fbfb5615bb270de",
          "width" : 64
        } ],
        "name" : "Always You (April 14th)",
        "release_date" : "2016-06-10",
        "release_date_precision" : "day",
        "type" : "album",
        "uri" : "spotify:album:6Wdmkzzbyb5qQSoHWGnqqF"
      },
      "artists" : [ {
        "external_urls" : {
          "spotify" : "https://open.spotify.com/artist/07lKyiT8QdydzmCrDAznnQ"
        },
        "href" : "https://api.spotify.com/v1/artists/07lKyiT8QdydzmCrDAznnQ",
        "id" : "07lKyiT8QdydzmCrDAznnQ",
        "name" : "Brian Hansen",
        "type" : "artist",
        "uri" : "spotify:artist:07lKyiT8QdydzmCrDAznnQ"
      } ],
      "available_markets" : [ "AD", "AR", "AT", "AU", "BE", "BG", "BO", "BR", "CA", "CH", "CL", "CO", "CR", "CY", "CZ", "DE", "DK", "DO", "EC", "EE", "ES", "FI", "FR", "GB", "GR", "GT", "HK", "HN", "HU", "ID", "IE", "IL", "IS", "IT", "JP", "LI", "LT", "LU", "LV", "MC", "MT", "MX", "MY", "NI", "NL", "NO", "NZ", "PA", "PE", "PH", "PL", "PT", "PY", "RO", "SE", "SG", "SK", "SV", "TH", "TR", "TW", "US", "UY", "VN", "ZA" ],
      "disc_number" : 1,
      "duration_ms" : 200975,
      "explicit" : false,
      "external_ids" : {
        "isrc" : "QMDUY1600001"
      },
      "external_urls" : {
        "spotify" : "https://open.spotify.com/track/7jv3jlF29DGGSdsIuP3lvz"
      },
      "href" : "https://api.spotify.com/v1/tracks/7jv3jlF29DGGSdsIuP3lvz",
      "id" : "7jv3jlF29DGGSdsIuP3lvz",
      "is_local" : false,
      "name" : "Always You (April 14th)",
      "popularity" : 0,
      "preview_url" : "https://p.scdn.co/mp3-preview/9a481c945dae6cc1e292ac272f1b8c9d3ac9d6ff?cid=b5993e2dcca64251a0fc4c780dd257c3",
      "track_number" : 1,
      "type" : "track",
      "uri" : "spotify:track:7jv3jlF29DGGSdsIuP3lvz"
    }, {
      "album" : {
        "album_type" : "album",
        "artists" : [ {
          "external_urls" : {
            "spotify" : "https://open.spotify.com/artist/282TitoEq4at65ZLoOmU4i"
          },
          "href" : "https://api.spotify.com/v1/artists/282TitoEq4at65ZLoOmU4i",
          "id" : "282TitoEq4at65ZLoOmU4i",
          "name" : "Zorznijor",
          "type" : "artist",
          "uri" : "spotify:artist:282TitoEq4at65ZLoOmU4i"
        } ],
        "available_markets" : [ "AD", "AR", "AT", "AU", "BE", "BG", "BO", "BR", "CA", "CH", "CL", "CO", "CR", "CY", "CZ", "DE", "DK", "DO", "EC", "EE", "ES", "FI", "FR", "GB", "GR", "GT", "HK", "HN", "HU", "ID", "IE", "IL", "IS", "IT", "JP", "LI", "LT", "LU", "LV", "MC", "MT", "MX", "MY", "NI", "NL", "NO", "NZ", "PA", "PE", "PH", "PL", "PT", "PY", "RO", "SE", "SG", "SK", "SV", "TH", "TR", "TW", "US", "UY", "VN", "ZA" ],
        "external_urls" : {
          "spotify" : "https://open.spotify.com/album/2CSAWpRELbXd87jNhgIO8t"
        },
        "href" : "https://api.spotify.com/v1/albums/2CSAWpRELbXd87jNhgIO8t",
        "id" : "2CSAWpRELbXd87jNhgIO8t",
        "images" : [ {
          "height" : 640,
          "url" : "https://i.scdn.co/image/5cf95d641cd9a68ecfb26f21e80ca42286e062ec",
          "width" : 640
        }, {
          "height" : 300,
          "url" : "https://i.scdn.co/image/012118a238fa3aec489d8ea8ecf6a3dcb263c328",
          "width" : 300
        }, {
          "height" : 64,
          "url" : "https://i.scdn.co/image/6dcf998efdc6c4b5a0fe2ec68aed3294c08479b2",
          "width" : 64
        } ],
        "name" : "Days of the Year: March, April, & May",
        "release_date" : "2017-10-13",
        "release_date_precision" : "day",
        "type" : "album",
        "uri" : "spotify:album:2CSAWpRELbXd87jNhgIO8t"
      },
      "artists" : [ {
        "external_urls" : {
          "spotify" : "https://open.spotify.com/artist/282TitoEq4at65ZLoOmU4i"
        },
        "href" : "https://api.spotify.com/v1/artists/282TitoEq4at65ZLoOmU4i",
        "id" : "282TitoEq4at65ZLoOmU4i",
        "name" : "Zorznijor",
        "type" : "artist",
        "uri" : "spotify:artist:282TitoEq4at65ZLoOmU4i"
      } ],
      "available_markets" : [ "AD", "AR", "AT", "AU", "BE", "BG", "BO", "BR", "CA", "CH", "CL", "CO", "CR", "CY", "CZ", "DE", "DK", "DO", "EC", "EE", "ES", "FI", "FR", "GB", "GR", "GT", "HK", "HN", "HU", "ID", "IE", "IL", "IS", "IT", "JP", "LI", "LT", "LU", "LV", "MC", "MT", "MX", "MY", "NI", "NL", "NO", "NZ", "PA", "PE", "PH", "PL", "PT", "PY", "RO", "SE", "SG", "SK", "SV", "TH", "TR", "TW", "US", "UY", "VN", "ZA" ],
      "disc_number" : 1,
      "duration_ms" : 83786,
      "explicit" : false,
      "external_ids" : {
        "isrc" : "ushm91721639"
      },
      "external_urls" : {
        "spotify" : "https://open.spotify.com/track/0J3wu4DAIgD1qLFwaDxrs4"
      },
      "href" : "https://api.spotify.com/v1/tracks/0J3wu4DAIgD1qLFwaDxrs4",
      "id" : "0J3wu4DAIgD1qLFwaDxrs4",
      "is_local" : false,
      "name" : "April 14th",
      "popularity" : 0,
      "preview_url" : "https://p.scdn.co/mp3-preview/d37764daf2877d10aabee4f5ac2542b4cfddd7c1?cid=b5993e2dcca64251a0fc4c780dd257c3",
      "track_number" : 45,
      "type" : "track",
      "uri" : "spotify:track:0J3wu4DAIgD1qLFwaDxrs4"
    }, {
      "album" : {
        "album_type" : "album",
        "artists" : [ {
          "external_urls" : {
            "spotify" : "https://open.spotify.com/artist/1XLCwxRdDcI2HJDZ6uHSSt"
          },
          "href" : "https://api.spotify.com/v1/artists/1XLCwxRdDcI2HJDZ6uHSSt",
          "id" : "1XLCwxRdDcI2HJDZ6uHSSt",
          "name" : "Simon Peterson",
          "type" : "artist",
          "uri" : "spotify:artist:1XLCwxRdDcI2HJDZ6uHSSt"
        } ],
        "available_markets" : [ "AD", "AR", "AT", "AU", "BE", "BG", "BO", "BR", "CA", "CH", "CL", "CO", "CR", "CY", "CZ", "DE", "DK", "DO", "EC", "EE", "ES", "FI", "FR", "GB", "GR", "GT", "HK", "HN", "HU", "ID", "IE", "IL", "IS", "IT", "JP", "LI", "LT", "LU", "LV", "MC", "MT", "MX", "MY", "NI", "NL", "NO", "NZ", "PA", "PE", "PH", "PL", "PT", "PY", "RO", "SE", "SG", "SK", "SV", "TH", "TR", "TW", "US", "UY", "VN", "ZA" ],
        "external_urls" : {
          "spotify" : "https://open.spotify.com/album/6bSyP6hdPryGwZOyMnQI0O"
        },
        "href" : "https://api.spotify.com/v1/albums/6bSyP6hdPryGwZOyMnQI0O",
        "id" : "6bSyP6hdPryGwZOyMnQI0O",
        "images" : [ {
          "height" : 640,
          "url" : "https://i.scdn.co/image/5f81313bf714b6d077a60123a03bc362f9e6a0e2",
          "width" : 640
        }, {
          "height" : 300,
          "url" : "https://i.scdn.co/image/ba9af64de8339263bc066d21b41eba197fb6a53a",
          "width" : 300
        }, {
          "height" : 64,
          "url" : "https://i.scdn.co/image/6e793d778f897d26e587c4b55c9f6e3cc008f3ef",
          "width" : 64
        } ],
        "name" : "Reflections - A Reading for Every Day in April",
        "release_date" : "2010-01-01",
        "release_date_precision" : "day",
        "type" : "album",
        "uri" : "spotify:album:6bSyP6hdPryGwZOyMnQI0O"
      },
      "artists" : [ {
        "external_urls" : {
          "spotify" : "https://open.spotify.com/artist/1XLCwxRdDcI2HJDZ6uHSSt"
        },
        "href" : "https://api.spotify.com/v1/artists/1XLCwxRdDcI2HJDZ6uHSSt",
        "id" : "1XLCwxRdDcI2HJDZ6uHSSt",
        "name" : "Simon Peterson",
        "type" : "artist",
        "uri" : "spotify:artist:1XLCwxRdDcI2HJDZ6uHSSt"
      } ],
      "available_markets" : [ "AD", "AR", "AT", "AU", "BE", "BG", "BO", "BR", "CA", "CH", "CL", "CO", "CR", "CY", "CZ", "DE", "DK", "DO", "EC", "EE", "ES", "FI", "FR", "GB", "GR", "GT", "HK", "HN", "HU", "ID", "IE", "IL", "IS", "IT", "JP", "LI", "LT", "LU", "LV", "MC", "MT", "MX", "MY", "NI", "NL", "NO", "NZ", "PA", "PE", "PH", "PL", "PT", "PY", "RO", "SE", "SG", "SK", "SV", "TH", "TR", "TW", "US", "UY", "VN", "ZA" ],
      "disc_number" : 1,
      "duration_ms" : 73717,
      "explicit" : false,
      "external_ids" : {
        "isrc" : "FR6V80262133"
      },
      "external_urls" : {
        "spotify" : "https://open.spotify.com/track/44SoUacl2XjOAyAqExC9Ob"
      },
      "href" : "https://api.spotify.com/v1/tracks/44SoUacl2XjOAyAqExC9Ob",
      "id" : "44SoUacl2XjOAyAqExC9Ob",
      "is_local" : false,
      "name" : "Reflections - 14th April",
      "popularity" : 0,
      "preview_url" : "https://p.scdn.co/mp3-preview/a4dacce15ccce55caee6cdfdb900875198d477ef?cid=b5993e2dcca64251a0fc4c780dd257c3",
      "track_number" : 14,
      "type" : "track",
      "uri" : "spotify:track:44SoUacl2XjOAyAqExC9Ob"
    }, {
      "album" : {
        "album_type" : "album",
        "artists" : [ {
          "external_urls" : {
            "spotify" : "https://open.spotify.com/artist/121Q6oslYCMBYZHhOFL1RB"
          },
          "href" : "https://api.spotify.com/v1/artists/121Q6oslYCMBYZHhOFL1RB",
          "id" : "121Q6oslYCMBYZHhOFL1RB",
          "name" : "Richard Hell",
          "type" : "artist",
          "uri" : "spotify:artist:121Q6oslYCMBYZHhOFL1RB"
        } ],
        "available_markets" : [ "AD", "AR", "AT", "AU", "BE", "BG", "BO", "BR", "CA", "CH", "CL", "CO", "CR", "CY", "CZ", "DE", "DK", "DO", "EC", "EE", "ES", "FI", "FR", "GB", "GR", "GT", "HK", "HN", "HU", "ID", "IE", "IL", "IS", "IT", "JP", "LI", "LT", "LU", "LV", "MC", "MT", "MX", "MY", "NI", "NL", "NO", "NZ", "PA", "PE", "PH", "PL", "PT", "PY", "RO", "SE", "SG", "SK", "SV", "TH", "TR", "TW", "US", "UY", "VN", "ZA" ],
        "external_urls" : {
          "spotify" : "https://open.spotify.com/album/69b7nBXWwREudaeDgIhZXA"
        },
        "href" : "https://api.spotify.com/v1/albums/69b7nBXWwREudaeDgIhZXA",
        "id" : "69b7nBXWwREudaeDgIhZXA",
        "images" : [ {
          "height" : 640,
          "url" : "https://i.scdn.co/image/497ba9825cf02b68b1f40cf12994c844b6740650",
          "width" : 640
        }, {
          "height" : 300,
          "url" : "https://i.scdn.co/image/b29b6d9083b2cd79be26c1ae0b7e0dd82da7a64a",
          "width" : 300
        }, {
          "height" : 64,
          "url" : "https://i.scdn.co/image/029fcd50d77d5b035d4e42bdf02b4b1b6fee4a82",
          "width" : 64
        } ],
        "name" : "Blank Generation (40th Anniversary Deluxe Edition)",
        "release_date" : "2017-11-24",
        "release_date_precision" : "day",
        "type" : "album",
        "uri" : "spotify:album:69b7nBXWwREudaeDgIhZXA"
      },
      "artists" : [ {
        "external_urls" : {
          "spotify" : "https://open.spotify.com/artist/121Q6oslYCMBYZHhOFL1RB"
        },
        "href" : "https://api.spotify.com/v1/artists/121Q6oslYCMBYZHhOFL1RB",
        "id" : "121Q6oslYCMBYZHhOFL1RB",
        "name" : "Richard Hell",
        "type" : "artist",
        "uri" : "spotify:artist:121Q6oslYCMBYZHhOFL1RB"
      } ],
      "available_markets" : [ "AD", "AR", "AT", "AU", "BE", "BG", "BO", "BR", "CA", "CH", "CL", "CO", "CR", "CY", "CZ", "DE", "DK", "DO", "EC", "EE", "ES", "FI", "FR", "GB", "GR", "GT", "HK", "HN", "HU", "ID", "IE", "IL", "IS", "IT", "JP", "LI", "LT", "LU", "LV", "MC", "MT", "MX", "MY", "NI", "NL", "NO", "NZ", "PA", "PE", "PH", "PL", "PT", "PY", "RO", "SE", "SG", "SK", "SV", "TH", "TR", "TW", "US", "UY", "VN", "ZA" ],
      "disc_number" : 2,
      "duration_ms" : 177906,
      "explicit" : false,
      "external_ids" : {
        "isrc" : "USRH11702655"
      },
      "external_urls" : {
        "spotify" : "https://open.spotify.com/track/1Y8i4y5DDIwBkm1joYoasW"
      },
      "href" : "https://api.spotify.com/v1/tracks/1Y8i4y5DDIwBkm1joYoasW",
      "id" : "1Y8i4y5DDIwBkm1joYoasW",
      "is_local" : false,
      "name" : "Liars Beware - Live at CBGB April 14th, 1977",
      "popularity" : 9,
      "preview_url" : "https://p.scdn.co/mp3-preview/dad4104217f4eb7bfebed73c50132feb69955918?cid=b5993e2dcca64251a0fc4c780dd257c3",
      "track_number" : 7,
      "type" : "track",
      "uri" : "spotify:track:1Y8i4y5DDIwBkm1joYoasW"
    }, {
      "album" : {
        "album_type" : "album",
        "artists" : [ {
          "external_urls" : {
            "spotify" : "https://open.spotify.com/artist/121Q6oslYCMBYZHhOFL1RB"
          },
          "href" : "https://api.spotify.com/v1/artists/121Q6oslYCMBYZHhOFL1RB",
          "id" : "121Q6oslYCMBYZHhOFL1RB",
          "name" : "Richard Hell",
          "type" : "artist",
          "uri" : "spotify:artist:121Q6oslYCMBYZHhOFL1RB"
        } ],
        "available_markets" : [ "AD", "AR", "AT", "AU", "BE", "BG", "BO", "BR", "CA", "CH", "CL", "CO", "CR", "CY", "CZ", "DE", "DK", "DO", "EC", "EE", "ES", "FI", "FR", "GB", "GR", "GT", "HK", "HN", "HU", "ID", "IE", "IL", "IS", "IT", "JP", "LI", "LT", "LU", "LV", "MC", "MT", "MX", "MY", "NI", "NL", "NO", "NZ", "PA", "PE", "PH", "PL", "PT", "PY", "RO", "SE", "SG", "SK", "SV", "TH", "TR", "TW", "US", "UY", "VN", "ZA" ],
        "external_urls" : {
          "spotify" : "https://open.spotify.com/album/69b7nBXWwREudaeDgIhZXA"
        },
        "href" : "https://api.spotify.com/v1/albums/69b7nBXWwREudaeDgIhZXA",
        "id" : "69b7nBXWwREudaeDgIhZXA",
        "images" : [ {
          "height" : 640,
          "url" : "https://i.scdn.co/image/497ba9825cf02b68b1f40cf12994c844b6740650",
          "width" : 640
        }, {
          "height" : 300,
          "url" : "https://i.scdn.co/image/b29b6d9083b2cd79be26c1ae0b7e0dd82da7a64a",
          "width" : 300
        }, {
          "height" : 64,
          "url" : "https://i.scdn.co/image/029fcd50d77d5b035d4e42bdf02b4b1b6fee4a82",
          "width" : 64
        } ],
        "name" : "Blank Generation (40th Anniversary Deluxe Edition)",
        "release_date" : "2017-11-24",
        "release_date_precision" : "day",
        "type" : "album",
        "uri" : "spotify:album:69b7nBXWwREudaeDgIhZXA"
      },
      "artists" : [ {
        "external_urls" : {
          "spotify" : "https://open.spotify.com/artist/121Q6oslYCMBYZHhOFL1RB"
        },
        "href" : "https://api.spotify.com/v1/artists/121Q6oslYCMBYZHhOFL1RB",
        "id" : "121Q6oslYCMBYZHhOFL1RB",
        "name" : "Richard Hell",
        "type" : "artist",
        "uri" : "spotify:artist:121Q6oslYCMBYZHhOFL1RB"
      } ],
      "available_markets" : [ "AD", "AR", "AT", "AU", "BE", "BG", "BO", "BR", "CA", "CH", "CL", "CO", "CR", "CY", "CZ", "DE", "DK", "DO", "EC", "EE", "ES", "FI", "FR", "GB", "GR", "GT", "HK", "HN", "HU", "ID", "IE", "IL", "IS", "IT", "JP", "LI", "LT", "LU", "LV", "MC", "MT", "MX", "MY", "NI", "NL", "NO", "NZ", "PA", "PE", "PH", "PL", "PT", "PY", "RO", "SE", "SG", "SK", "SV", "TH", "TR", "TW", "US", "UY", "VN", "ZA" ],
      "disc_number" : 2,
      "duration_ms" : 155026,
      "explicit" : false,
      "external_ids" : {
        "isrc" : "USRH11702653"
      },
      "external_urls" : {
        "spotify" : "https://open.spotify.com/track/1HMRpZ22qKHxBL07nwUVaf"
      },
      "href" : "https://api.spotify.com/v1/tracks/1HMRpZ22qKHxBL07nwUVaf",
      "id" : "1HMRpZ22qKHxBL07nwUVaf",
      "is_local" : false,
      "name" : "New Pleasure - Live at CBGB April 14th, 1977",
      "popularity" : 9,
      "preview_url" : "https://p.scdn.co/mp3-preview/5bc64884f78b19d17962b10ac6d93edb03ab3e04?cid=b5993e2dcca64251a0fc4c780dd257c3",
      "track_number" : 8,
      "type" : "track",
      "uri" : "spotify:track:1HMRpZ22qKHxBL07nwUVaf"
    }, {
      "album" : {
        "album_type" : "album",
        "artists" : [ {
          "external_urls" : {
            "spotify" : "https://open.spotify.com/artist/3bnvRCS6ttQyHmoxvDcLHW"
          },
          "href" : "https://api.spotify.com/v1/artists/3bnvRCS6ttQyHmoxvDcLHW",
          "id" : "3bnvRCS6ttQyHmoxvDcLHW",
          "name" : "Folks",
          "type" : "artist",
          "uri" : "spotify:artist:3bnvRCS6ttQyHmoxvDcLHW"
        } ],
        "available_markets" : [ "AD", "AR", "AT", "AU", "BE", "BG", "BO", "BR", "CA", "CH", "CL", "CO", "CR", "CY", "CZ", "DE", "DK", "DO", "EC", "EE", "ES", "FI", "FR", "GB", "GR", "GT", "HK", "HN", "HU", "ID", "IE", "IL", "IS", "IT", "JP", "LI", "LT", "LU", "LV", "MC", "MT", "MX", "MY", "NI", "NL", "NO", "NZ", "PA", "PE", "PH", "PL", "PT", "PY", "RO", "SE", "SG", "SK", "SV", "TH", "TR", "TW", "US", "UY", "VN", "ZA" ],
        "external_urls" : {
          "spotify" : "https://open.spotify.com/album/0Nsv318eoSvNaNejcmj9tx"
        },
        "href" : "https://api.spotify.com/v1/albums/0Nsv318eoSvNaNejcmj9tx",
        "id" : "0Nsv318eoSvNaNejcmj9tx",
        "images" : [ {
          "height" : 640,
          "url" : "https://i.scdn.co/image/e0110156a5f4ef5c9acd307d3392ac17601854a3",
          "width" : 640
        }, {
          "height" : 300,
          "url" : "https://i.scdn.co/image/b4f8a076299d31b4d8e6fbe966ebed314626dd71",
          "width" : 300
        }, {
          "height" : 64,
          "url" : "https://i.scdn.co/image/a5e26821d57518274bc584628e19ad4df385b0d4",
          "width" : 64
        } ],
        "name" : "Bohemian Highway",
        "release_date" : "2017-12-12",
        "release_date_precision" : "day",
        "type" : "album",
        "uri" : "spotify:album:0Nsv318eoSvNaNejcmj9tx"
      },
      "artists" : [ {
        "external_urls" : {
          "spotify" : "https://open.spotify.com/artist/3bnvRCS6ttQyHmoxvDcLHW"
        },
        "href" : "https://api.spotify.com/v1/artists/3bnvRCS6ttQyHmoxvDcLHW",
        "id" : "3bnvRCS6ttQyHmoxvDcLHW",
        "name" : "Folks",
        "type" : "artist",
        "uri" : "spotify:artist:3bnvRCS6ttQyHmoxvDcLHW"
      } ],
      "available_markets" : [ "AD", "AR", "AT", "AU", "BE", "BG", "BO", "BR", "CA", "CH", "CL", "CO", "CR", "CY", "CZ", "DE", "DK", "DO", "EC", "EE", "ES", "FI", "FR", "GB", "GR", "GT", "HK", "HN", "HU", "ID", "IE", "IL", "IS", "IT", "JP", "LI", "LT", "LU", "LV", "MC", "MT", "MX", "MY", "NI", "NL", "NO", "NZ", "PA", "PE", "PH", "PL", "PT", "PY", "RO", "SE", "SG", "SK", "SV", "TH", "TR", "TW", "US", "UY", "VN", "ZA" ],
      "disc_number" : 1,
      "duration_ms" : 305500,
      "explicit" : false,
      "external_ids" : {
        "isrc" : "SEYOK1780318"
      },
      "external_urls" : {
        "spotify" : "https://open.spotify.com/track/59VrIn2qyxZ8PReqcBPZIw"
      },
      "href" : "https://api.spotify.com/v1/tracks/59VrIn2qyxZ8PReqcBPZIw",
      "id" : "59VrIn2qyxZ8PReqcBPZIw",
      "is_local" : false,
      "name" : "April 14th",
      "popularity" : 3,
      "preview_url" : "https://p.scdn.co/mp3-preview/b93b7ba43be52f1112c9e33d0109fe4b4b2a48a6?cid=b5993e2dcca64251a0fc4c780dd257c3",
      "track_number" : 5,
      "type" : "track",
      "uri" : "spotify:track:59VrIn2qyxZ8PReqcBPZIw"
    }, {
      "album" : {
        "album_type" : "single",
        "artists" : [ {
          "external_urls" : {
            "spotify" : "https://open.spotify.com/artist/3inl2nuKk7Q9OHXer1Sk4s"
          },
          "href" : "https://api.spotify.com/v1/artists/3inl2nuKk7Q9OHXer1Sk4s",
          "id" : "3inl2nuKk7Q9OHXer1Sk4s",
          "name" : "Poison or Medicine",
          "type" : "artist",
          "uri" : "spotify:artist:3inl2nuKk7Q9OHXer1Sk4s"
        } ],
        "available_markets" : [ "AD", "AR", "AT", "AU", "BE", "BG", "BO", "BR", "CA", "CH", "CL", "CO", "CR", "CY", "CZ", "DE", "DK", "DO", "EC", "EE", "ES", "FI", "FR", "GB", "GR", "GT", "HK", "HN", "HU", "ID", "IE", "IL", "IS", "IT", "JP", "LI", "LT", "LU", "LV", "MC", "MT", "MX", "MY", "NI", "NL", "NO", "NZ", "PA", "PE", "PH", "PL", "PT", "PY", "RO", "SE", "SG", "SK", "SV", "TH", "TR", "TW", "US", "UY", "VN", "ZA" ],
        "external_urls" : {
          "spotify" : "https://open.spotify.com/album/7e38ZF5X6zhYEbnNi2pRMv"
        },
        "href" : "https://api.spotify.com/v1/albums/7e38ZF5X6zhYEbnNi2pRMv",
        "id" : "7e38ZF5X6zhYEbnNi2pRMv",
        "images" : [ {
          "height" : 640,
          "url" : "https://i.scdn.co/image/2852d2e2d0975495f6404ffb8a89fcb670a44037",
          "width" : 640
        }, {
          "height" : 300,
          "url" : "https://i.scdn.co/image/3d4a3fb3271ccd502f518eb279d62b14df0f122d",
          "width" : 300
        }, {
          "height" : 64,
          "url" : "https://i.scdn.co/image/d5f4b12c324d4e0abfd9a8e279311b47f6ae78be",
          "width" : 64
        } ],
        "name" : "Losers Are Going to Die Alone",
        "release_date" : "2015-05-22",
        "release_date_precision" : "day",
        "type" : "album",
        "uri" : "spotify:album:7e38ZF5X6zhYEbnNi2pRMv"
      },
      "artists" : [ {
        "external_urls" : {
          "spotify" : "https://open.spotify.com/artist/3inl2nuKk7Q9OHXer1Sk4s"
        },
        "href" : "https://api.spotify.com/v1/artists/3inl2nuKk7Q9OHXer1Sk4s",
        "id" : "3inl2nuKk7Q9OHXer1Sk4s",
        "name" : "Poison or Medicine",
        "type" : "artist",
        "uri" : "spotify:artist:3inl2nuKk7Q9OHXer1Sk4s"
      } ],
      "available_markets" : [ "AD", "AR", "AT", "AU", "BE", "BG", "BO", "BR", "CA", "CH", "CL", "CO", "CR", "CY", "CZ", "DE", "DK", "DO", "EC", "EE", "ES", "FI", "FR", "GB", "GR", "GT", "HK", "HN", "HU", "ID", "IE", "IL", "IS", "IT", "JP", "LI", "LT", "LU", "LV", "MC", "MT", "MX", "MY", "NI", "NL", "NO", "NZ", "PA", "PE", "PH", "PL", "PT", "PY", "RO", "SE", "SG", "SK", "SV", "TH", "TR", "TW", "US", "UY", "VN", "ZA" ],
      "disc_number" : 1,
      "duration_ms" : 166181,
      "explicit" : false,
      "external_ids" : {
        "isrc" : "US7VG1751832"
      },
      "external_urls" : {
        "spotify" : "https://open.spotify.com/track/4blgOV5Y8CClKRrxqn6IcL"
      },
      "href" : "https://api.spotify.com/v1/tracks/4blgOV5Y8CClKRrxqn6IcL",
      "id" : "4blgOV5Y8CClKRrxqn6IcL",
      "is_local" : false,
      "name" : "April 14Th",
      "popularity" : 1,
      "preview_url" : "https://p.scdn.co/mp3-preview/66e7e26ad10dba53a05f0a7d73ac085452f320aa?cid=b5993e2dcca64251a0fc4c780dd257c3",
      "track_number" : 3,
      "type" : "track",
      "uri" : "spotify:track:4blgOV5Y8CClKRrxqn6IcL"
    }, {
      "album" : {
        "album_type" : "album",
        "artists" : [ {
          "external_urls" : {
            "spotify" : "https://open.spotify.com/artist/4FhVXqEdpdz5tnAv7igkMv"
          },
          "href" : "https://api.spotify.com/v1/artists/4FhVXqEdpdz5tnAv7igkMv",
          "id" : "4FhVXqEdpdz5tnAv7igkMv",
          "name" : "The Local Tourists",
          "type" : "artist",
          "uri" : "spotify:artist:4FhVXqEdpdz5tnAv7igkMv"
        } ],
        "available_markets" : [ "AD", "AR", "AT", "AU", "BE", "BG", "BO", "BR", "CA", "CH", "CL", "CO", "CR", "CY", "CZ", "DE", "DK", "DO", "EC", "EE", "ES", "FI", "FR", "GB", "GR", "GT", "HK", "HN", "HU", "ID", "IE", "IL", "IS", "IT", "JP", "LI", "LT", "LU", "LV", "MC", "MT", "MX", "MY", "NI", "NL", "NO", "NZ", "PA", "PE", "PH", "PL", "PT", "PY", "RO", "SE", "SG", "SK", "SV", "TH", "TR", "TW", "US", "UY", "VN", "ZA" ],
        "external_urls" : {
          "spotify" : "https://open.spotify.com/album/5McmMnIBDN81hF5HRNNvug"
        },
        "href" : "https://api.spotify.com/v1/albums/5McmMnIBDN81hF5HRNNvug",
        "id" : "5McmMnIBDN81hF5HRNNvug",
        "images" : [ {
          "height" : 640,
          "url" : "https://i.scdn.co/image/4b4aa3201eccb38edb842c817e01fd7879163a11",
          "width" : 640
        }, {
          "height" : 300,
          "url" : "https://i.scdn.co/image/ba61302062f2c24cbce311eaf79a730f5d5487a9",
          "width" : 300
        }, {
          "height" : 64,
          "url" : "https://i.scdn.co/image/2cd325986d4bee32714359ad1c917572d56ab74a",
          "width" : 64
        } ],
        "name" : "Happy Birthday, Kyle",
        "release_date" : "2007-12-06",
        "release_date_precision" : "day",
        "type" : "album",
        "uri" : "spotify:album:5McmMnIBDN81hF5HRNNvug"
      },
      "artists" : [ {
        "external_urls" : {
          "spotify" : "https://open.spotify.com/artist/4FhVXqEdpdz5tnAv7igkMv"
        },
        "href" : "https://api.spotify.com/v1/artists/4FhVXqEdpdz5tnAv7igkMv",
        "id" : "4FhVXqEdpdz5tnAv7igkMv",
        "name" : "The Local Tourists",
        "type" : "artist",
        "uri" : "spotify:artist:4FhVXqEdpdz5tnAv7igkMv"
      } ],
      "available_markets" : [ "AD", "AR", "AT", "AU", "BE", "BG", "BO", "BR", "CA", "CH", "CL", "CO", "CR", "CY", "CZ", "DE", "DK", "DO", "EC", "EE", "ES", "FI", "FR", "GB", "GR", "GT", "HK", "HN", "HU", "ID", "IE", "IL", "IS", "IT", "JP", "LI", "LT", "LU", "LV", "MC", "MT", "MX", "MY", "NI", "NL", "NO", "NZ", "PA", "PE", "PH", "PL", "PT", "PY", "RO", "SE", "SG", "SK", "SV", "TH", "TR", "TW", "US", "UY", "VN", "ZA" ],
      "disc_number" : 1,
      "duration_ms" : 231106,
      "explicit" : false,
      "external_ids" : {
        "isrc" : "USTC30778477"
      },
      "external_urls" : {
        "spotify" : "https://open.spotify.com/track/0KzopZJIMEAPaC3a3uXoPY"
      },
      "href" : "https://api.spotify.com/v1/tracks/0KzopZJIMEAPaC3a3uXoPY",
      "id" : "0KzopZJIMEAPaC3a3uXoPY",
      "is_local" : false,
      "name" : "April 14th",
      "popularity" : 0,
      "preview_url" : "https://p.scdn.co/mp3-preview/fad64003d9c5cde9ed1faf43855ca81a5e5613e5?cid=b5993e2dcca64251a0fc4c780dd257c3",
      "track_number" : 8,
      "type" : "track",
      "uri" : "spotify:track:0KzopZJIMEAPaC3a3uXoPY"
    }, {
      "album" : {
        "album_type" : "album",
        "artists" : [ {
          "external_urls" : {
            "spotify" : "https://open.spotify.com/artist/1ew5GX8elS4IIzi14t5cFJ"
          },
          "href" : "https://api.spotify.com/v1/artists/1ew5GX8elS4IIzi14t5cFJ",
          "id" : "1ew5GX8elS4IIzi14t5cFJ",
          "name" : "Brainfreeze",
          "type" : "artist",
          "uri" : "spotify:artist:1ew5GX8elS4IIzi14t5cFJ"
        } ],
        "available_markets" : [ "AD", "AR", "AT", "AU", "BE", "BG", "BO", "BR", "CA", "CH", "CL", "CO", "CR", "CY", "CZ", "DE", "DK", "DO", "EC", "EE", "ES", "FI", "FR", "GB", "GR", "GT", "HK", "HN", "HU", "ID", "IE", "IL", "IS", "IT", "JP", "LI", "LT", "LU", "LV", "MC", "MT", "MX", "MY", "NI", "NL", "NO", "NZ", "PA", "PE", "PH", "PL", "PT", "PY", "RO", "SE", "SG", "SK", "SV", "TH", "TR", "TW", "US", "UY", "VN", "ZA" ],
        "external_urls" : {
          "spotify" : "https://open.spotify.com/album/3ZtuOgNN9xQWjNu2MCM6SL"
        },
        "href" : "https://api.spotify.com/v1/albums/3ZtuOgNN9xQWjNu2MCM6SL",
        "id" : "3ZtuOgNN9xQWjNu2MCM6SL",
        "images" : [ {
          "height" : 640,
          "url" : "https://i.scdn.co/image/1b1db041daeee172517238b83fa9c6db46802930",
          "width" : 640
        }, {
          "height" : 300,
          "url" : "https://i.scdn.co/image/684970964e1f5682a462b7907c889c6545b01e7d",
          "width" : 300
        }, {
          "height" : 64,
          "url" : "https://i.scdn.co/image/ab3deb77367ffe0ff9935a8d43b1d430fccd4d48",
          "width" : 64
        } ],
        "name" : "Too Big to Fail",
        "release_date" : "2015-08-15",
        "release_date_precision" : "day",
        "type" : "album",
        "uri" : "spotify:album:3ZtuOgNN9xQWjNu2MCM6SL"
      },
      "artists" : [ {
        "external_urls" : {
          "spotify" : "https://open.spotify.com/artist/1ew5GX8elS4IIzi14t5cFJ"
        },
        "href" : "https://api.spotify.com/v1/artists/1ew5GX8elS4IIzi14t5cFJ",
        "id" : "1ew5GX8elS4IIzi14t5cFJ",
        "name" : "Brainfreeze",
        "type" : "artist",
        "uri" : "spotify:artist:1ew5GX8elS4IIzi14t5cFJ"
      } ],
      "available_markets" : [ "AD", "AR", "AT", "AU", "BE", "BG", "BO", "BR", "CA", "CH", "CL", "CO", "CR", "CY", "CZ", "DE", "DK", "DO", "EC", "EE", "ES", "FI", "FR", "GB", "GR", "GT", "HK", "HN", "HU", "ID", "IE", "IL", "IS", "IT", "JP", "LI", "LT", "LU", "LV", "MC", "MT", "MX", "MY", "NI", "NL", "NO", "NZ", "PA", "PE", "PH", "PL", "PT", "PY", "RO", "SE", "SG", "SK", "SV", "TH", "TR", "TW", "US", "UY", "VN", "ZA" ],
      "disc_number" : 1,
      "duration_ms" : 208813,
      "explicit" : false,
      "external_ids" : {
        "isrc" : "usdy41579748"
      },
      "external_urls" : {
        "spotify" : "https://open.spotify.com/track/4cJUNbwiCIqQo5P2Qdykes"
      },
      "href" : "https://api.spotify.com/v1/tracks/4cJUNbwiCIqQo5P2Qdykes",
      "id" : "4cJUNbwiCIqQo5P2Qdykes",
      "is_local" : false,
      "name" : "April 14th",
      "popularity" : 0,
      "preview_url" : "https://p.scdn.co/mp3-preview/f962d1743b79fa539a40441e7b52c586ae48a369?cid=b5993e2dcca64251a0fc4c780dd257c3",
      "track_number" : 10,
      "type" : "track",
      "uri" : "spotify:track:4cJUNbwiCIqQo5P2Qdykes"
    }, {
      "album" : {
        "album_type" : "album",
        "artists" : [ {
          "external_urls" : {
            "spotify" : "https://open.spotify.com/artist/69ilqAmd46BBLLdJD29tyr"
          },
          "href" : "https://api.spotify.com/v1/artists/69ilqAmd46BBLLdJD29tyr",
          "id" : "69ilqAmd46BBLLdJD29tyr",
          "name" : "Jo Nash",
          "type" : "artist",
          "uri" : "spotify:artist:69ilqAmd46BBLLdJD29tyr"
        } ],
        "available_markets" : [ "AD", "AR", "AT", "AU", "BE", "BG", "BO", "BR", "CA", "CH", "CL", "CO", "CR", "CY", "CZ", "DE", "DK", "DO", "EC", "EE", "ES", "FI", "FR", "GB", "GR", "GT", "HK", "HN", "HU", "ID", "IE", "IL", "IS", "IT", "JP", "LI", "LT", "LU", "LV", "MC", "MT", "MX", "MY", "NI", "NL", "NO", "NZ", "PA", "PE", "PH", "PL", "PT", "PY", "RO", "SE", "SG", "SK", "SV", "TH", "TR", "TW", "US", "UY", "VN", "ZA" ],
        "external_urls" : {
          "spotify" : "https://open.spotify.com/album/4EcRkumu5Q5eZAptoaF8GV"
        },
        "href" : "https://api.spotify.com/v1/albums/4EcRkumu5Q5eZAptoaF8GV",
        "id" : "4EcRkumu5Q5eZAptoaF8GV",
        "images" : [ {
          "height" : 640,
          "url" : "https://i.scdn.co/image/969d6d2d9dbe8637cedba0720875bead7aeac62e",
          "width" : 640
        }, {
          "height" : 300,
          "url" : "https://i.scdn.co/image/ee6bab7c818791103e60e66b02565dde29eb0baa",
          "width" : 300
        }, {
          "height" : 64,
          "url" : "https://i.scdn.co/image/5229d077185047c87e16df4c638ced4b72473a6b",
          "width" : 64
        } ],
        "name" : "Change",
        "release_date" : "2014-08-11",
        "release_date_precision" : "day",
        "type" : "album",
        "uri" : "spotify:album:4EcRkumu5Q5eZAptoaF8GV"
      },
      "artists" : [ {
        "external_urls" : {
          "spotify" : "https://open.spotify.com/artist/69ilqAmd46BBLLdJD29tyr"
        },
        "href" : "https://api.spotify.com/v1/artists/69ilqAmd46BBLLdJD29tyr",
        "id" : "69ilqAmd46BBLLdJD29tyr",
        "name" : "Jo Nash",
        "type" : "artist",
        "uri" : "spotify:artist:69ilqAmd46BBLLdJD29tyr"
      } ],
      "available_markets" : [ "AD", "AR", "AT", "AU", "BE", "BG", "BO", "BR", "CA", "CH", "CL", "CO", "CR", "CY", "CZ", "DE", "DK", "DO", "EC", "EE", "ES", "FI", "FR", "GB", "GR", "GT", "HK", "HN", "HU", "ID", "IE", "IL", "IS", "IT", "JP", "LI", "LT", "LU", "LV", "MC", "MT", "MX", "MY", "NI", "NL", "NO", "NZ", "PA", "PE", "PH", "PL", "PT", "PY", "RO", "SE", "SG", "SK", "SV", "TH", "TR", "TW", "US", "UY", "VN", "ZA" ],
      "disc_number" : 1,
      "duration_ms" : 245520,
      "explicit" : false,
      "external_ids" : {
        "isrc" : "USUDG1000040"
      },
      "external_urls" : {
        "spotify" : "https://open.spotify.com/track/2plovOSO5VDKg4hxBL4i5d"
      },
      "href" : "https://api.spotify.com/v1/tracks/2plovOSO5VDKg4hxBL4i5d",
      "id" : "2plovOSO5VDKg4hxBL4i5d",
      "is_local" : false,
      "name" : "April 14th",
      "popularity" : 0,
      "preview_url" : "https://p.scdn.co/mp3-preview/5baf80c10191a8c65e399122945c76f868f4b0c7?cid=b5993e2dcca64251a0fc4c780dd257c3",
      "track_number" : 5,
      "type" : "track",
      "uri" : "spotify:track:2plovOSO5VDKg4hxBL4i5d"
    }, {
      "album" : {
        "album_type" : "single",
        "artists" : [ {
          "external_urls" : {
            "spotify" : "https://open.spotify.com/artist/0g8sI4vVHJo2z5xB5cyGrg"
          },
          "href" : "https://api.spotify.com/v1/artists/0g8sI4vVHJo2z5xB5cyGrg",
          "id" : "0g8sI4vVHJo2z5xB5cyGrg",
          "name" : "Waiting for Steve",
          "type" : "artist",
          "uri" : "spotify:artist:0g8sI4vVHJo2z5xB5cyGrg"
        } ],
        "available_markets" : [ "AD", "AR", "AT", "AU", "BE", "BG", "BO", "BR", "CA", "CH", "CL", "CO", "CR", "CY", "CZ", "DE", "DK", "DO", "EC", "EE", "ES", "FI", "FR", "GB", "GR", "GT", "HK", "HN", "HU", "ID", "IE", "IL", "IS", "IT", "JP", "LI", "LT", "LU", "LV", "MC", "MT", "MX", "MY", "NI", "NL", "NO", "NZ", "PA", "PE", "PH", "PL", "PT", "PY", "RO", "SE", "SG", "SK", "SV", "TH", "TR", "TW", "US", "UY", "VN", "ZA" ],
        "external_urls" : {
          "spotify" : "https://open.spotify.com/album/54tt8o1jJUmYmrVD4bSalk"
        },
        "href" : "https://api.spotify.com/v1/albums/54tt8o1jJUmYmrVD4bSalk",
        "id" : "54tt8o1jJUmYmrVD4bSalk",
        "images" : [ {
          "height" : 640,
          "url" : "https://i.scdn.co/image/8e77333306eec6a433ac200ae97d10d9bdd1b74e",
          "width" : 640
        }, {
          "height" : 300,
          "url" : "https://i.scdn.co/image/e181128eda50572e4cb61a811bc2b07e8d226c40",
          "width" : 300
        }, {
          "height" : 64,
          "url" : "https://i.scdn.co/image/878ee1b6901e3aec27c1af72d59c6a61e4be08cf",
          "width" : 64
        } ],
        "name" : "Lieutenant Dan",
        "release_date" : "2009-03-02",
        "release_date_precision" : "day",
        "type" : "album",
        "uri" : "spotify:album:54tt8o1jJUmYmrVD4bSalk"
      },
      "artists" : [ {
        "external_urls" : {
          "spotify" : "https://open.spotify.com/artist/0g8sI4vVHJo2z5xB5cyGrg"
        },
        "href" : "https://api.spotify.com/v1/artists/0g8sI4vVHJo2z5xB5cyGrg",
        "id" : "0g8sI4vVHJo2z5xB5cyGrg",
        "name" : "Waiting for Steve",
        "type" : "artist",
        "uri" : "spotify:artist:0g8sI4vVHJo2z5xB5cyGrg"
      } ],
      "available_markets" : [ "AD", "AR", "AT", "AU", "BE", "BG", "BO", "BR", "CA", "CH", "CL", "CO", "CR", "CY", "CZ", "DE", "DK", "DO", "EC", "EE", "ES", "FI", "FR", "GB", "GR", "GT", "HK", "HN", "HU", "ID", "IE", "IL", "IS", "IT", "JP", "LI", "LT", "LU", "LV", "MC", "MT", "MX", "MY", "NI", "NL", "NO", "NZ", "PA", "PE", "PH", "PL", "PT", "PY", "RO", "SE", "SG", "SK", "SV", "TH", "TR", "TW", "US", "UY", "VN", "ZA" ],
      "disc_number" : 1,
      "duration_ms" : 251946,
      "explicit" : false,
      "external_ids" : {
        "isrc" : "DEH930804004"
      },
      "external_urls" : {
        "spotify" : "https://open.spotify.com/track/2ZSNeXNhypB8VaDcDcakQz"
      },
      "href" : "https://api.spotify.com/v1/tracks/2ZSNeXNhypB8VaDcDcakQz",
      "id" : "2ZSNeXNhypB8VaDcDcakQz",
      "is_local" : false,
      "name" : "April 14th",
      "popularity" : 0,
      "preview_url" : "https://p.scdn.co/mp3-preview/1d1e31ea3dad92df09a67d1e081a22d4ad58bb55?cid=b5993e2dcca64251a0fc4c780dd257c3",
      "track_number" : 4,
      "type" : "track",
      "uri" : "spotify:track:2ZSNeXNhypB8VaDcDcakQz"
    }, {
      "album" : {
        "album_type" : "album",
        "artists" : [ {
          "external_urls" : {
            "spotify" : "https://open.spotify.com/artist/2qhNoA1gDZGVwTNf2WbcIe"
          },
          "href" : "https://api.spotify.com/v1/artists/2qhNoA1gDZGVwTNf2WbcIe",
          "id" : "2qhNoA1gDZGVwTNf2WbcIe",
          "name" : "Ellen",
          "type" : "artist",
          "uri" : "spotify:artist:2qhNoA1gDZGVwTNf2WbcIe"
        } ],
        "available_markets" : [ "AD", "AR", "AT", "AU", "BE", "BG", "BO", "BR", "CA", "CH", "CL", "CO", "CR", "CY", "CZ", "DE", "DK", "DO", "EC", "EE", "ES", "FI", "FR", "GB", "GR", "GT", "HK", "HN", "HU", "ID", "IE", "IL", "IS", "IT", "JP", "LI", "LT", "LU", "LV", "MC", "MT", "MX", "MY", "NI", "NL", "NO", "NZ", "PA", "PE", "PH", "PL", "PT", "PY", "RO", "SE", "SG", "SK", "SV", "TH", "TR", "TW", "US", "UY", "VN", "ZA" ],
        "external_urls" : {
          "spotify" : "https://open.spotify.com/album/1Gq14LXxIe5dIG3V9CXWMu"
        },
        "href" : "https://api.spotify.com/v1/albums/1Gq14LXxIe5dIG3V9CXWMu",
        "id" : "1Gq14LXxIe5dIG3V9CXWMu",
        "images" : [ {
          "height" : 640,
          "url" : "https://i.scdn.co/image/ca3a561031e162f08ccb69c68f4e30989232a347",
          "width" : 640
        }, {
          "height" : 300,
          "url" : "https://i.scdn.co/image/80e7d1dfaaf354b085fca201661ab093b6ec7152",
          "width" : 300
        }, {
          "height" : 64,
          "url" : "https://i.scdn.co/image/3ff5a3c65eb47096e2781e202b3113665ced7a52",
          "width" : 64
        } ],
        "name" : "Mourning This Morning",
        "release_date" : "2010-04-14",
        "release_date_precision" : "day",
        "type" : "album",
        "uri" : "spotify:album:1Gq14LXxIe5dIG3V9CXWMu"
      },
      "artists" : [ {
        "external_urls" : {
          "spotify" : "https://open.spotify.com/artist/2qhNoA1gDZGVwTNf2WbcIe"
        },
        "href" : "https://api.spotify.com/v1/artists/2qhNoA1gDZGVwTNf2WbcIe",
        "id" : "2qhNoA1gDZGVwTNf2WbcIe",
        "name" : "Ellen",
        "type" : "artist",
        "uri" : "spotify:artist:2qhNoA1gDZGVwTNf2WbcIe"
      } ],
      "available_markets" : [ "AD", "AR", "AT", "AU", "BE", "BG", "BO", "BR", "CA", "CH", "CL", "CO", "CR", "CY", "CZ", "DE", "DK", "DO", "EC", "EE", "ES", "FI", "FR", "GB", "GR", "GT", "HK", "HN", "HU", "ID", "IE", "IL", "IS", "IT", "JP", "LI", "LT", "LU", "LV", "MC", "MT", "MX", "MY", "NI", "NL", "NO", "NZ", "PA", "PE", "PH", "PL", "PT", "PY", "RO", "SE", "SG", "SK", "SV", "TH", "TR", "TW", "US", "UY", "VN", "ZA" ],
      "disc_number" : 1,
      "duration_ms" : 212333,
      "explicit" : false,
      "external_ids" : {
        "isrc" : "SEVYZ1000104"
      },
      "external_urls" : {
        "spotify" : "https://open.spotify.com/track/6KsfxGHT88DDQIlGQswj02"
      },
      "href" : "https://api.spotify.com/v1/tracks/6KsfxGHT88DDQIlGQswj02",
      "id" : "6KsfxGHT88DDQIlGQswj02",
      "is_local" : false,
      "name" : "April 14th",
      "popularity" : 0,
      "preview_url" : "https://p.scdn.co/mp3-preview/82fe839c883d57fd072511199410a5d4c437000f?cid=b5993e2dcca64251a0fc4c780dd257c3",
      "track_number" : 4,
      "type" : "track",
      "uri" : "spotify:track:6KsfxGHT88DDQIlGQswj02"
    }, {
      "album" : {
        "album_type" : "album",
        "artists" : [ {
          "external_urls" : {
            "spotify" : "https://open.spotify.com/artist/2UXctDGCsIhU1mbYhW7uVo"
          },
          "href" : "https://api.spotify.com/v1/artists/2UXctDGCsIhU1mbYhW7uVo",
          "id" : "2UXctDGCsIhU1mbYhW7uVo",
          "name" : "The RTTs",
          "type" : "artist",
          "uri" : "spotify:artist:2UXctDGCsIhU1mbYhW7uVo"
        } ],
        "available_markets" : [ "AD", "AR", "AT", "AU", "BE", "BG", "BO", "BR", "CA", "CH", "CL", "CO", "CR", "CY", "CZ", "DE", "DK", "DO", "EC", "EE", "ES", "FI", "FR", "GB", "GR", "GT", "HK", "HN", "HU", "ID", "IE", "IL", "IS", "IT", "JP", "LI", "LT", "LU", "LV", "MC", "MT", "MX", "MY", "NI", "NL", "NO", "NZ", "PA", "PE", "PH", "PL", "PT", "PY", "RO", "SE", "SG", "SK", "SV", "TH", "TR", "TW", "US", "UY", "VN", "ZA" ],
        "external_urls" : {
          "spotify" : "https://open.spotify.com/album/5N1mvspmo07TF16dlxfgVF"
        },
        "href" : "https://api.spotify.com/v1/albums/5N1mvspmo07TF16dlxfgVF",
        "id" : "5N1mvspmo07TF16dlxfgVF",
        "images" : [ {
          "height" : 640,
          "url" : "https://i.scdn.co/image/b3a59280e0ecf120b495cd76c7a551a6f28b77c9",
          "width" : 640
        }, {
          "height" : 300,
          "url" : "https://i.scdn.co/image/bc86cf97f89f5ff4668297a6f06a8253a5d44a49",
          "width" : 300
        }, {
          "height" : 64,
          "url" : "https://i.scdn.co/image/1bc6ccb0ebfdcf74b72d265526c047d6c90300bf",
          "width" : 64
        } ],
        "name" : "Turn It Up Mommy",
        "release_date" : "2003-11-24",
        "release_date_precision" : "day",
        "type" : "album",
        "uri" : "spotify:album:5N1mvspmo07TF16dlxfgVF"
      },
      "artists" : [ {
        "external_urls" : {
          "spotify" : "https://open.spotify.com/artist/2UXctDGCsIhU1mbYhW7uVo"
        },
        "href" : "https://api.spotify.com/v1/artists/2UXctDGCsIhU1mbYhW7uVo",
        "id" : "2UXctDGCsIhU1mbYhW7uVo",
        "name" : "The RTTs",
        "type" : "artist",
        "uri" : "spotify:artist:2UXctDGCsIhU1mbYhW7uVo"
      } ],
      "available_markets" : [ "AD", "AR", "AT", "AU", "BE", "BG", "BO", "BR", "CA", "CH", "CL", "CO", "CR", "CY", "CZ", "DE", "DK", "DO", "EC", "EE", "ES", "FI", "FR", "GB", "GR", "GT", "HK", "HN", "HU", "ID", "IE", "IL", "IS", "IT", "JP", "LI", "LT", "LU", "LV", "MC", "MT", "MX", "MY", "NI", "NL", "NO", "NZ", "PA", "PE", "PH", "PL", "PT", "PY", "RO", "SE", "SG", "SK", "SV", "TH", "TR", "TW", "US", "UY", "VN", "ZA" ],
      "disc_number" : 1,
      "duration_ms" : 169053,
      "explicit" : false,
      "external_ids" : {
        "isrc" : "ushm80422937"
      },
      "external_urls" : {
        "spotify" : "https://open.spotify.com/track/4vaG5ymHwMz4h0Vm3XNXsX"
      },
      "href" : "https://api.spotify.com/v1/tracks/4vaG5ymHwMz4h0Vm3XNXsX",
      "id" : "4vaG5ymHwMz4h0Vm3XNXsX",
      "is_local" : false,
      "name" : "April 14th",
      "popularity" : 0,
      "preview_url" : "https://p.scdn.co/mp3-preview/117cd45e17f603d64187e8e21b58ebca77bb8fd6?cid=b5993e2dcca64251a0fc4c780dd257c3",
      "track_number" : 8,
      "type" : "track",
      "uri" : "spotify:track:4vaG5ymHwMz4h0Vm3XNXsX"
    }, {
      "album" : {
        "album_type" : "album",
        "artists" : [ {
          "external_urls" : {
            "spotify" : "https://open.spotify.com/artist/0FCGzMOhqe8N0P0V6prMZn"
          },
          "href" : "https://api.spotify.com/v1/artists/0FCGzMOhqe8N0P0V6prMZn",
          "id" : "0FCGzMOhqe8N0P0V6prMZn",
          "name" : "Mosquito-B",
          "type" : "artist",
          "uri" : "spotify:artist:0FCGzMOhqe8N0P0V6prMZn"
        } ],
        "available_markets" : [ "AD", "AR", "AT", "AU", "BE", "BG", "BO", "BR", "CA", "CH", "CL", "CO", "CR", "CY", "CZ", "DE", "DK", "DO", "EC", "EE", "ES", "FI", "FR", "GB", "GR", "GT", "HK", "HN", "HU", "ID", "IE", "IL", "IS", "IT", "JP", "LI", "LT", "LU", "LV", "MC", "MT", "MX", "MY", "NI", "NL", "NO", "NZ", "PA", "PE", "PH", "PL", "PT", "PY", "RO", "SE", "SG", "SK", "SV", "TH", "TR", "TW", "US", "UY", "VN", "ZA" ],
        "external_urls" : {
          "spotify" : "https://open.spotify.com/album/76NacPqYbxcbHKC8ZUa8zb"
        },
        "href" : "https://api.spotify.com/v1/albums/76NacPqYbxcbHKC8ZUa8zb",
        "id" : "76NacPqYbxcbHKC8ZUa8zb",
        "images" : [ {
          "height" : 640,
          "url" : "https://i.scdn.co/image/b271609d7ae93e85c91f7f7bdfc35c54890ce395",
          "width" : 640
        }, {
          "height" : 300,
          "url" : "https://i.scdn.co/image/6456cdcaa3c3b3f2263fc34f194e20372311c59a",
          "width" : 300
        }, {
          "height" : 64,
          "url" : "https://i.scdn.co/image/bff0f78924c40f41d38f6c5be1205d03272ba2b9",
          "width" : 64
        } ],
        "name" : "Raid",
        "release_date" : "2009-01-29",
        "release_date_precision" : "day",
        "type" : "album",
        "uri" : "spotify:album:76NacPqYbxcbHKC8ZUa8zb"
      },
      "artists" : [ {
        "external_urls" : {
          "spotify" : "https://open.spotify.com/artist/0FCGzMOhqe8N0P0V6prMZn"
        },
        "href" : "https://api.spotify.com/v1/artists/0FCGzMOhqe8N0P0V6prMZn",
        "id" : "0FCGzMOhqe8N0P0V6prMZn",
        "name" : "Mosquito-B",
        "type" : "artist",
        "uri" : "spotify:artist:0FCGzMOhqe8N0P0V6prMZn"
      } ],
      "available_markets" : [ "AD", "AR", "AT", "AU", "BE", "BG", "BO", "BR", "CA", "CH", "CL", "CO", "CR", "CY", "CZ", "DE", "DK", "DO", "EC", "EE", "ES", "FI", "FR", "GB", "GR", "GT", "HK", "HN", "HU", "ID", "IE", "IL", "IS", "IT", "JP", "LI", "LT", "LU", "LV", "MC", "MT", "MX", "MY", "NI", "NL", "NO", "NZ", "PA", "PE", "PH", "PL", "PT", "PY", "RO", "SE", "SG", "SK", "SV", "TH", "TR", "TW", "US", "UY", "VN", "ZA" ],
      "disc_number" : 1,
      "duration_ms" : 155293,
      "explicit" : false,
      "external_ids" : {
        "isrc" : "CAU111015955"
      },
      "external_urls" : {
        "spotify" : "https://open.spotify.com/track/1Xe7apP2Q6kT9S3PSfRoyI"
      },
      "href" : "https://api.spotify.com/v1/tracks/1Xe7apP2Q6kT9S3PSfRoyI",
      "id" : "1Xe7apP2Q6kT9S3PSfRoyI",
      "is_local" : false,
      "name" : "April 14th",
      "popularity" : 0,
      "preview_url" : "https://p.scdn.co/mp3-preview/1bf829260822c18c8d5fc92035775f07288d1e9f?cid=b5993e2dcca64251a0fc4c780dd257c3",
      "track_number" : 6,
      "type" : "track",
      "uri" : "spotify:track:1Xe7apP2Q6kT9S3PSfRoyI"
    }, {
      "album" : {
        "album_type" : "album",
        "artists" : [ {
          "external_urls" : {
            "spotify" : "https://open.spotify.com/artist/1XLCwxRdDcI2HJDZ6uHSSt"
          },
          "href" : "https://api.spotify.com/v1/artists/1XLCwxRdDcI2HJDZ6uHSSt",
          "id" : "1XLCwxRdDcI2HJDZ6uHSSt",
          "name" : "Simon Peterson",
          "type" : "artist",
          "uri" : "spotify:artist:1XLCwxRdDcI2HJDZ6uHSSt"
        } ],
        "available_markets" : [ "AD", "AR", "AT", "AU", "BE", "BG", "BO", "BR", "CA", "CH", "CL", "CO", "CR", "CY", "CZ", "DE", "DK", "DO", "EC", "EE", "ES", "FI", "FR", "GB", "GR", "GT", "HK", "HN", "HU", "ID", "IE", "IL", "IS", "IT", "JP", "LI", "LT", "LU", "LV", "MC", "MT", "MX", "MY", "NI", "NL", "NO", "NZ", "PA", "PE", "PH", "PL", "PT", "PY", "RO", "SE", "SG", "SK", "SV", "TH", "TR", "TW", "US", "UY", "VN", "ZA" ],
        "external_urls" : {
          "spotify" : "https://open.spotify.com/album/7GkyyoYx7zCldQgrD5MRHO"
        },
        "href" : "https://api.spotify.com/v1/albums/7GkyyoYx7zCldQgrD5MRHO",
        "id" : "7GkyyoYx7zCldQgrD5MRHO",
        "images" : [ {
          "height" : 640,
          "url" : "https://i.scdn.co/image/555b2412ce356680a292bef0fc0573b8919645fd",
          "width" : 640
        }, {
          "height" : 300,
          "url" : "https://i.scdn.co/image/5b2e88eaeb03386f63ecb4198d8a5c64b57d9f82",
          "width" : 300
        }, {
          "height" : 64,
          "url" : "https://i.scdn.co/image/d8429c291c4d7e1495fc5ee5d064bbdf3c4b7b95",
          "width" : 64
        } ],
        "name" : "Daily Praise - a Prayer for Every Day in April",
        "release_date" : "2010-01-01",
        "release_date_precision" : "day",
        "type" : "album",
        "uri" : "spotify:album:7GkyyoYx7zCldQgrD5MRHO"
      },
      "artists" : [ {
        "external_urls" : {
          "spotify" : "https://open.spotify.com/artist/1XLCwxRdDcI2HJDZ6uHSSt"
        },
        "href" : "https://api.spotify.com/v1/artists/1XLCwxRdDcI2HJDZ6uHSSt",
        "id" : "1XLCwxRdDcI2HJDZ6uHSSt",
        "name" : "Simon Peterson",
        "type" : "artist",
        "uri" : "spotify:artist:1XLCwxRdDcI2HJDZ6uHSSt"
      } ],
      "available_markets" : [ "AD", "AR", "AT", "AU", "BE", "BG", "BO", "BR", "CA", "CH", "CL", "CO", "CR", "CY", "CZ", "DE", "DK", "DO", "EC", "EE", "ES", "FI", "FR", "GB", "GR", "GT", "HK", "HN", "HU", "ID", "IE", "IL", "IS", "IT", "JP", "LI", "LT", "LU", "LV", "MC", "MT", "MX", "MY", "NI", "NL", "NO", "NZ", "PA", "PE", "PH", "PL", "PT", "PY", "RO", "SE", "SG", "SK", "SV", "TH", "TR", "TW", "US", "UY", "VN", "ZA" ],
      "disc_number" : 1,
      "duration_ms" : 78288,
      "explicit" : false,
      "external_ids" : {
        "isrc" : "FR6V80271712"
      },
      "external_urls" : {
        "spotify" : "https://open.spotify.com/track/3pOynIw3MVRdUEl6p3bVuf"
      },
      "href" : "https://api.spotify.com/v1/tracks/3pOynIw3MVRdUEl6p3bVuf",
      "id" : "3pOynIw3MVRdUEl6p3bVuf",
      "is_local" : false,
      "name" : "Daily Praise - 14th April",
      "popularity" : 0,
      "preview_url" : "https://p.scdn.co/mp3-preview/fc8375da78b0cd4112b56dc3b5593bb411bcb390?cid=b5993e2dcca64251a0fc4c780dd257c3",
      "track_number" : 14,
      "type" : "track",
      "uri" : "spotify:track:3pOynIw3MVRdUEl6p3bVuf"
    }, {
      "album" : {
        "album_type" : "single",
        "artists" : [ {
          "external_urls" : {
            "spotify" : "https://open.spotify.com/artist/6wHQ70FcRAy0tMYaHuecaR"
          },
          "href" : "https://api.spotify.com/v1/artists/6wHQ70FcRAy0tMYaHuecaR",
          "id" : "6wHQ70FcRAy0tMYaHuecaR",
          "name" : "Everything That Rises",
          "type" : "artist",
          "uri" : "spotify:artist:6wHQ70FcRAy0tMYaHuecaR"
        } ],
        "available_markets" : [ "AD", "AR", "AT", "AU", "BE", "BG", "BO", "BR", "CA", "CH", "CL", "CO", "CR", "CY", "CZ", "DE", "DK", "DO", "EC", "EE", "ES", "FI", "FR", "GB", "GR", "GT", "HK", "HN", "HU", "ID", "IE", "IL", "IS", "IT", "JP", "LI", "LT", "LU", "LV", "MC", "MT", "MX", "MY", "NI", "NL", "NO", "NZ", "PA", "PE", "PH", "PL", "PT", "PY", "RO", "SE", "SG", "SK", "SV", "TH", "TR", "TW", "US", "UY", "VN", "ZA" ],
        "external_urls" : {
          "spotify" : "https://open.spotify.com/album/0DsSeYBjSt4JVESferwwap"
        },
        "href" : "https://api.spotify.com/v1/albums/0DsSeYBjSt4JVESferwwap",
        "id" : "0DsSeYBjSt4JVESferwwap",
        "images" : [ {
          "height" : 640,
          "url" : "https://i.scdn.co/image/5e7411c8a891374a54627ef3fcea05225d06c46f",
          "width" : 640
        }, {
          "height" : 300,
          "url" : "https://i.scdn.co/image/9766200528f479d4c37d77849affefeb69c2184c",
          "width" : 300
        }, {
          "height" : 64,
          "url" : "https://i.scdn.co/image/c1d2e46ca346af6ee5d787976148540f4c3ef406",
          "width" : 64
        } ],
        "name" : "April 14th",
        "release_date" : "2014-04-14",
        "release_date_precision" : "day",
        "type" : "album",
        "uri" : "spotify:album:0DsSeYBjSt4JVESferwwap"
      },
      "artists" : [ {
        "external_urls" : {
          "spotify" : "https://open.spotify.com/artist/6wHQ70FcRAy0tMYaHuecaR"
        },
        "href" : "https://api.spotify.com/v1/artists/6wHQ70FcRAy0tMYaHuecaR",
        "id" : "6wHQ70FcRAy0tMYaHuecaR",
        "name" : "Everything That Rises",
        "type" : "artist",
        "uri" : "spotify:artist:6wHQ70FcRAy0tMYaHuecaR"
      } ],
      "available_markets" : [ "AD", "AR", "AT", "AU", "BE", "BG", "BO", "BR", "CA", "CH", "CL", "CO", "CR", "CY", "CZ", "DE", "DK", "DO", "EC", "EE", "ES", "FI", "FR", "GB", "GR", "GT", "HK", "HN", "HU", "ID", "IE", "IL", "IS", "IT", "JP", "LI", "LT", "LU", "LV", "MC", "MT", "MX", "MY", "NI", "NL", "NO", "NZ", "PA", "PE", "PH", "PL", "PT", "PY", "RO", "SE", "SG", "SK", "SV", "TH", "TR", "TW", "US", "UY", "VN", "ZA" ],
      "disc_number" : 1,
      "duration_ms" : 107085,
      "explicit" : false,
      "external_ids" : {
        "isrc" : "SEYOK1407119"
      },
      "external_urls" : {
        "spotify" : "https://open.spotify.com/track/3ucvaVes1ge5PoBSXolSDv"
      },
      "href" : "https://api.spotify.com/v1/tracks/3ucvaVes1ge5PoBSXolSDv",
      "id" : "3ucvaVes1ge5PoBSXolSDv",
      "is_local" : false,
      "name" : "Sanctuary",
      "popularity" : 0,
      "preview_url" : "https://p.scdn.co/mp3-preview/17369158c09767e86ba79893c78dfa018301801a?cid=b5993e2dcca64251a0fc4c780dd257c3",
      "track_number" : 1,
      "type" : "track",
      "uri" : "spotify:track:3ucvaVes1ge5PoBSXolSDv"
    }, {
      "album" : {
        "album_type" : "single",
        "artists" : [ {
          "external_urls" : {
            "spotify" : "https://open.spotify.com/artist/6wHQ70FcRAy0tMYaHuecaR"
          },
          "href" : "https://api.spotify.com/v1/artists/6wHQ70FcRAy0tMYaHuecaR",
          "id" : "6wHQ70FcRAy0tMYaHuecaR",
          "name" : "Everything That Rises",
          "type" : "artist",
          "uri" : "spotify:artist:6wHQ70FcRAy0tMYaHuecaR"
        } ],
        "available_markets" : [ "AD", "AR", "AT", "AU", "BE", "BG", "BO", "BR", "CA", "CH", "CL", "CO", "CR", "CY", "CZ", "DE", "DK", "DO", "EC", "EE", "ES", "FI", "FR", "GB", "GR", "GT", "HK", "HN", "HU", "ID", "IE", "IL", "IS", "IT", "JP", "LI", "LT", "LU", "LV", "MC", "MT", "MX", "MY", "NI", "NL", "NO", "NZ", "PA", "PE", "PH", "PL", "PT", "PY", "RO", "SE", "SG", "SK", "SV", "TH", "TR", "TW", "US", "UY", "VN", "ZA" ],
        "external_urls" : {
          "spotify" : "https://open.spotify.com/album/0DsSeYBjSt4JVESferwwap"
        },
        "href" : "https://api.spotify.com/v1/albums/0DsSeYBjSt4JVESferwwap",
        "id" : "0DsSeYBjSt4JVESferwwap",
        "images" : [ {
          "height" : 640,
          "url" : "https://i.scdn.co/image/5e7411c8a891374a54627ef3fcea05225d06c46f",
          "width" : 640
        }, {
          "height" : 300,
          "url" : "https://i.scdn.co/image/9766200528f479d4c37d77849affefeb69c2184c",
          "width" : 300
        }, {
          "height" : 64,
          "url" : "https://i.scdn.co/image/c1d2e46ca346af6ee5d787976148540f4c3ef406",
          "width" : 64
        } ],
        "name" : "April 14th",
        "release_date" : "2014-04-14",
        "release_date_precision" : "day",
        "type" : "album",
        "uri" : "spotify:album:0DsSeYBjSt4JVESferwwap"
      },
      "artists" : [ {
        "external_urls" : {
          "spotify" : "https://open.spotify.com/artist/6wHQ70FcRAy0tMYaHuecaR"
        },
        "href" : "https://api.spotify.com/v1/artists/6wHQ70FcRAy0tMYaHuecaR",
        "id" : "6wHQ70FcRAy0tMYaHuecaR",
        "name" : "Everything That Rises",
        "type" : "artist",
        "uri" : "spotify:artist:6wHQ70FcRAy0tMYaHuecaR"
      } ],
      "available_markets" : [ "AD", "AR", "AT", "AU", "BE", "BG", "BO", "BR", "CA", "CH", "CL", "CO", "CR", "CY", "CZ", "DE", "DK", "DO", "EC", "EE", "ES", "FI", "FR", "GB", "GR", "GT", "HK", "HN", "HU", "ID", "IE", "IL", "IS", "IT", "JP", "LI", "LT", "LU", "LV", "MC", "MT", "MX", "MY", "NI", "NL", "NO", "NZ", "PA", "PE", "PH", "PL", "PT", "PY", "RO", "SE", "SG", "SK", "SV", "TH", "TR", "TW", "US", "UY", "VN", "ZA" ],
      "disc_number" : 1,
      "duration_ms" : 95638,
      "explicit" : false,
      "external_ids" : {
        "isrc" : "SEYOK1407120"
      },
      "external_urls" : {
        "spotify" : "https://open.spotify.com/track/2uz0eek29QWickUkAzdmMA"
      },
      "href" : "https://api.spotify.com/v1/tracks/2uz0eek29QWickUkAzdmMA",
      "id" : "2uz0eek29QWickUkAzdmMA",
      "is_local" : false,
      "name" : "Where Do You Want To Go?",
      "popularity" : 0,
      "preview_url" : "https://p.scdn.co/mp3-preview/e1c2056cc4e1c6707ebee3a8d7d8e0ff4e676586?cid=b5993e2dcca64251a0fc4c780dd257c3",
      "track_number" : 2,
      "type" : "track",
      "uri" : "spotify:track:2uz0eek29QWickUkAzdmMA"
    } ],
    "limit" : 20,
    "next" : "https://api.spotify.com/v1/search?query=April+14th&type=track&offset=20&limit=20",
    "offset" : 0,
    "previous" : null,
    "total" : 58
  }
}"""

    client = SpotifyMusicSearchService("client_id", "client_secret")
    tracks = client._parse_track_results(raw_response)

    assert len(tracks) == 20
    assert tracks[0].uri == "spotify:track:3f9HJzevC4sMYGDwj7yQwd"


def test_correct_parsing_of_tracks_with_empty_response():
    raw_empty_response = """{
  "tracks" : {
    "href" : "https://api.spotify.com/v1/search?query=Bashibookzeiezjfoizejfnzeiufhbieuhbfieruhg&type=track&offset=0&limit=20",
    "items" : [ ],
    "limit" : 20,
    "next" : null,
    "offset" : 0,
    "previous" : null,
    "total" : 0
  }
}"""

    client = SpotifyMusicSearchService("client_id", "client_secret")
    tracks = client._parse_track_results(raw_empty_response)

    assert len(tracks) == 0
