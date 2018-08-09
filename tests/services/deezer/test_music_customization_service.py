import pytest

from snipssonos.services.deezer.music_customization_service import DeezerCustomizationService


@pytest.fixture
def deezer_api_tracks_output():
    return '''{
        "data": [
            {
                "id": "536421002",
                "readable": true,
                "title": "SICKO MODE",
                "link": "https://www.deezer.com/track/536421002",
                "duration": "312",
                "rank": "310261",
                "explicit_lyrics": true,
                "time_add": 1533731032,
                "album": {
                    "id": "69804312",
                    "title": "ASTROWORLD",
                    "cover": "https://api.deezer.com/album/69804312/image",
                    "cover_small": "https://cdns-images.dzcdn.net/images/cover/7df7ac6028591a5622f24cf32a555510/56x56-000000-80-0-0.jpg",
                    "cover_medium": "https://cdns-images.dzcdn.net/images/cover/7df7ac6028591a5622f24cf32a555510/250x250-000000-80-0-0.jpg",
                    "cover_big": "https://cdns-images.dzcdn.net/images/cover/7df7ac6028591a5622f24cf32a555510/500x500-000000-80-0-0.jpg",
                    "cover_xl": "https://cdns-images.dzcdn.net/images/cover/7df7ac6028591a5622f24cf32a555510/1000x1000-000000-80-0-0.jpg",
                    "tracklist": "https://api.deezer.com/album/69804312/tracks",
                    "type": "album"
                },
                "artist": {
                    "id": "4495513",
                    "name": "Travis Scott",
                    "picture": "https://api.deezer.com/artist/4495513/image",
                    "picture_small": "https://cdns-images.dzcdn.net/images/artist/c1689f623450a7bf2e177b7564658a07/56x56-000000-80-0-0.jpg",
                    "picture_medium": "https://cdns-images.dzcdn.net/images/artist/c1689f623450a7bf2e177b7564658a07/250x250-000000-80-0-0.jpg",
                    "picture_big": "https://cdns-images.dzcdn.net/images/artist/c1689f623450a7bf2e177b7564658a07/500x500-000000-80-0-0.jpg",
                    "picture_xl": "https://cdns-images.dzcdn.net/images/artist/c1689f623450a7bf2e177b7564658a07/1000x1000-000000-80-0-0.jpg",
                    "tracklist": "https://api.deezer.com/artist/4495513/top?limit=50",
                    "type": "artist"
                },
                "type": "track"
            },
            {
                "id": "135949706",
                "readable": true,
                "title": "Tchoin",
                "link": "https://www.deezer.com/track/135949706",
                "duration": "156",
                "rank": "820530",
                "explicit_lyrics": true,
                "time_add": 1533826750,
                "album": {
                    "id": "14530576",
                    "title": "Okou Gnakouri",
                    "cover": "https://api.deezer.com/album/14530576/image",
                    "cover_small": "https://cdns-images.dzcdn.net/images/cover/74c25c24295c145b2cda08869b100f32/56x56-000000-80-0-0.jpg",
                    "cover_medium": "https://cdns-images.dzcdn.net/images/cover/74c25c24295c145b2cda08869b100f32/250x250-000000-80-0-0.jpg",
                    "cover_big": "https://cdns-images.dzcdn.net/images/cover/74c25c24295c145b2cda08869b100f32/500x500-000000-80-0-0.jpg",
                    "cover_xl": "https://cdns-images.dzcdn.net/images/cover/74c25c24295c145b2cda08869b100f32/1000x1000-000000-80-0-0.jpg",
                    "tracklist": "https://api.deezer.com/album/14530576/tracks",
                    "type": "album"
                },
                "artist": {
                    "id": "388973",
                    "name": "Kaaris",
                    "picture": "https://api.deezer.com/artist/388973/image",
                    "picture_small": "https://cdns-images.dzcdn.net/images/artist/c6d0e4bd4b7332480d580a56e531db5a/56x56-000000-80-0-0.jpg",
                    "picture_medium": "https://cdns-images.dzcdn.net/images/artist/c6d0e4bd4b7332480d580a56e531db5a/250x250-000000-80-0-0.jpg",
                    "picture_big": "https://cdns-images.dzcdn.net/images/artist/c6d0e4bd4b7332480d580a56e531db5a/500x500-000000-80-0-0.jpg",
                    "picture_xl": "https://cdns-images.dzcdn.net/images/artist/c6d0e4bd4b7332480d580a56e531db5a/1000x1000-000000-80-0-0.jpg",
                    "tracklist": "https://api.deezer.com/artist/388973/top?limit=50",
                    "type": "artist"
                },
                "type": "track"
            },
            {
                "id": "71678124",
                "readable": true,
                "title": "Zoo",
                "link": "https://www.deezer.com/track/71678124",
                "duration": "288",
                "rank": "660592",
                "explicit_lyrics": true,
                "time_add": 1533826804,
                "album": {
                    "id": "7042876",
                    "title": "Or Noir",
                    "cover": "https://api.deezer.com/album/7042876/image",
                    "cover_small": "https://cdns-images.dzcdn.net/images/cover/1592d2a42e992da187cb70f12994677d/56x56-000000-80-0-0.jpg",
                    "cover_medium": "https://cdns-images.dzcdn.net/images/cover/1592d2a42e992da187cb70f12994677d/250x250-000000-80-0-0.jpg",
                    "cover_big": "https://cdns-images.dzcdn.net/images/cover/1592d2a42e992da187cb70f12994677d/500x500-000000-80-0-0.jpg",
                    "cover_xl": "https://cdns-images.dzcdn.net/images/cover/1592d2a42e992da187cb70f12994677d/1000x1000-000000-80-0-0.jpg",
                    "tracklist": "https://api.deezer.com/album/7042876/tracks",
                    "type": "album"
                },
                "artist": {
                    "id": "388973",
                    "name": "Kaaris",
                    "picture": "https://api.deezer.com/artist/388973/image",
                    "picture_small": "https://cdns-images.dzcdn.net/images/artist/c6d0e4bd4b7332480d580a56e531db5a/56x56-000000-80-0-0.jpg",
                    "picture_medium": "https://cdns-images.dzcdn.net/images/artist/c6d0e4bd4b7332480d580a56e531db5a/250x250-000000-80-0-0.jpg",
                    "picture_big": "https://cdns-images.dzcdn.net/images/artist/c6d0e4bd4b7332480d580a56e531db5a/500x500-000000-80-0-0.jpg",
                    "picture_xl": "https://cdns-images.dzcdn.net/images/artist/c6d0e4bd4b7332480d580a56e531db5a/1000x1000-000000-80-0-0.jpg",
                    "tracklist": "https://api.deezer.com/artist/388973/top?limit=50",
                    "type": "artist"
                },
                "type": "track"
            }
        ],
        "checksum": "2ccb9c18caef7d4f1fd7b1bc746d8a54",
        "total": 3
    }'''


@pytest.fixture
def deezer_api_artists_output():
    return '''
    {
  "data": [
    {
      "id": "48",
      "name": "IAM",
      "link": "https://www.deezer.com/artist/48",
      "picture": "https://api.deezer.com/artist/48/image",
      "picture_small": "https://e-cdns-images.dzcdn.net/images/artist/254909d37a04abc8dafde9fc7500c836/56x56-000000-80-0-0.jpg",
      "picture_medium": "https://e-cdns-images.dzcdn.net/images/artist/254909d37a04abc8dafde9fc7500c836/250x250-000000-80-0-0.jpg",
      "picture_big": "https://e-cdns-images.dzcdn.net/images/artist/254909d37a04abc8dafde9fc7500c836/500x500-000000-80-0-0.jpg",
      "picture_xl": "https://e-cdns-images.dzcdn.net/images/artist/254909d37a04abc8dafde9fc7500c836/1000x1000-000000-80-0-0.jpg",
      "nb_album": 45,
      "nb_fan": 375126,
      "radio": true,
      "tracklist": "https://api.deezer.com/artist/48/top?limit=50",
      "time_add": 1533826722,
      "type": "artist"
    },
    {
      "id": "254",
      "name": "Damian Marley",
      "link": "https://www.deezer.com/artist/254",
      "picture": "https://api.deezer.com/artist/254/image",
      "picture_small": "https://e-cdns-images.dzcdn.net/images/artist/115bacd4f76f5a2a9dbfe2ad4026c798/56x56-000000-80-0-0.jpg",
      "picture_medium": "https://e-cdns-images.dzcdn.net/images/artist/115bacd4f76f5a2a9dbfe2ad4026c798/250x250-000000-80-0-0.jpg",
      "picture_big": "https://e-cdns-images.dzcdn.net/images/artist/115bacd4f76f5a2a9dbfe2ad4026c798/500x500-000000-80-0-0.jpg",
      "picture_xl": "https://e-cdns-images.dzcdn.net/images/artist/115bacd4f76f5a2a9dbfe2ad4026c798/1000x1000-000000-80-0-0.jpg",
      "nb_album": 14,
      "nb_fan": 1942562,
      "radio": true,
      "tracklist": "https://api.deezer.com/artist/254/top?limit=50",
      "time_add": 1533561250,
      "type": "artist"
    },
    {
      "id": "305",
      "name": "Kool & The Gang",
      "link": "https://www.deezer.com/artist/305",
      "picture": "https://api.deezer.com/artist/305/image",
      "picture_small": "https://e-cdns-images.dzcdn.net/images/artist//56x56-000000-80-0-0.jpg",
      "picture_medium": "https://e-cdns-images.dzcdn.net/images/artist//250x250-000000-80-0-0.jpg",
      "picture_big": "https://e-cdns-images.dzcdn.net/images/artist//500x500-000000-80-0-0.jpg",
      "picture_xl": "https://e-cdns-images.dzcdn.net/images/artist//1000x1000-000000-80-0-0.jpg",
      "nb_album": 110,
      "nb_fan": 381850,
      "radio": true,
      "tracklist": "https://api.deezer.com/artist/305/top?limit=50",
      "time_add": 1533561243,
      "type": "artist"
    },
    {
      "id": "390",
      "name": "Booba",
      "link": "https://www.deezer.com/artist/390",
      "picture": "https://api.deezer.com/artist/390/image",
      "picture_small": "https://e-cdns-images.dzcdn.net/images/artist/b354e3298214e7146a05b663f10b6346/56x56-000000-80-0-0.jpg",
      "picture_medium": "https://e-cdns-images.dzcdn.net/images/artist/b354e3298214e7146a05b663f10b6346/250x250-000000-80-0-0.jpg",
      "picture_big": "https://e-cdns-images.dzcdn.net/images/artist/b354e3298214e7146a05b663f10b6346/500x500-000000-80-0-0.jpg",
      "picture_xl": "https://e-cdns-images.dzcdn.net/images/artist/b354e3298214e7146a05b663f10b6346/1000x1000-000000-80-0-0.jpg",
      "nb_album": 43,
      "nb_fan": 3652318,
      "radio": true,
      "tracklist": "https://api.deezer.com/artist/390/top?limit=50",
      "time_add": 1533826740,
      "type": "artist"
    },
    {
      "id": "1342",
      "name": "Ray Charles",
      "link": "https://www.deezer.com/artist/1342",
      "picture": "https://api.deezer.com/artist/1342/image",
      "picture_small": "https://e-cdns-images.dzcdn.net/images/artist/67dd9cc17d6b974280821a20e3a48be5/56x56-000000-80-0-0.jpg",
      "picture_medium": "https://e-cdns-images.dzcdn.net/images/artist/67dd9cc17d6b974280821a20e3a48be5/250x250-000000-80-0-0.jpg",
      "picture_big": "https://e-cdns-images.dzcdn.net/images/artist/67dd9cc17d6b974280821a20e3a48be5/500x500-000000-80-0-0.jpg",
      "picture_xl": "https://e-cdns-images.dzcdn.net/images/artist/67dd9cc17d6b974280821a20e3a48be5/1000x1000-000000-80-0-0.jpg",
      "nb_album": 443,
      "nb_fan": 2152061,
      "radio": true,
      "tracklist": "https://api.deezer.com/artist/1342/top?limit=50",
      "time_add": 1533561233,
      "type": "artist"
    },
    {
      "id": "1910",
      "name": "Miles Davis",
      "link": "https://www.deezer.com/artist/1910",
      "picture": "https://api.deezer.com/artist/1910/image",
      "picture_small": "https://e-cdns-images.dzcdn.net/images/artist/8d13c0527064ba50cf0d0873f4f574dc/56x56-000000-80-0-0.jpg",
      "picture_medium": "https://e-cdns-images.dzcdn.net/images/artist/8d13c0527064ba50cf0d0873f4f574dc/250x250-000000-80-0-0.jpg",
      "picture_big": "https://e-cdns-images.dzcdn.net/images/artist/8d13c0527064ba50cf0d0873f4f574dc/500x500-000000-80-0-0.jpg",
      "picture_xl": "https://e-cdns-images.dzcdn.net/images/artist/8d13c0527064ba50cf0d0873f4f574dc/1000x1000-000000-80-0-0.jpg",
      "nb_album": 452,
      "nb_fan": 716927,
      "radio": true,
      "tracklist": "https://api.deezer.com/artist/1910/top?limit=50",
      "time_add": 1533826709,
      "type": "artist"
    },
    {
      "id": "3606",
      "name": "Yellowman",
      "link": "https://www.deezer.com/artist/3606",
      "picture": "https://api.deezer.com/artist/3606/image",
      "picture_small": "https://e-cdns-images.dzcdn.net/images/artist/d621bb98759731cea28e0ec32fc68170/56x56-000000-80-0-0.jpg",
      "picture_medium": "https://e-cdns-images.dzcdn.net/images/artist/d621bb98759731cea28e0ec32fc68170/250x250-000000-80-0-0.jpg",
      "picture_big": "https://e-cdns-images.dzcdn.net/images/artist/d621bb98759731cea28e0ec32fc68170/500x500-000000-80-0-0.jpg",
      "picture_xl": "https://e-cdns-images.dzcdn.net/images/artist/d621bb98759731cea28e0ec32fc68170/1000x1000-000000-80-0-0.jpg",
      "nb_album": 62,
      "nb_fan": 33143,
      "radio": true,
      "tracklist": "https://api.deezer.com/artist/3606/top?limit=50",
      "time_add": 1533826732,
      "type": "artist"
    },
    {
      "id": "4933",
      "name": "Roy Ayers",
      "link": "https://www.deezer.com/artist/4933",
      "picture": "https://api.deezer.com/artist/4933/image",
      "picture_small": "https://e-cdns-images.dzcdn.net/images/artist//56x56-000000-80-0-0.jpg",
      "picture_medium": "https://e-cdns-images.dzcdn.net/images/artist//250x250-000000-80-0-0.jpg",
      "picture_big": "https://e-cdns-images.dzcdn.net/images/artist//500x500-000000-80-0-0.jpg",
      "picture_xl": "https://e-cdns-images.dzcdn.net/images/artist//1000x1000-000000-80-0-0.jpg",
      "nb_album": 45,
      "nb_fan": 11593,
      "radio": true,
      "tracklist": "https://api.deezer.com/artist/4933/top?limit=50",
      "time_add": 1533826714,
      "type": "artist"
    },
    {
      "id": "10611",
      "name": "Keith Jarrett",
      "link": "https://www.deezer.com/artist/10611",
      "picture": "https://api.deezer.com/artist/10611/image",
      "picture_small": "https://e-cdns-images.dzcdn.net/images/artist/ba6d113f166bfb4cf4dc470ad012f2ba/56x56-000000-80-0-0.jpg",
      "picture_medium": "https://e-cdns-images.dzcdn.net/images/artist/ba6d113f166bfb4cf4dc470ad012f2ba/250x250-000000-80-0-0.jpg",
      "picture_big": "https://e-cdns-images.dzcdn.net/images/artist/ba6d113f166bfb4cf4dc470ad012f2ba/500x500-000000-80-0-0.jpg",
      "picture_xl": "https://e-cdns-images.dzcdn.net/images/artist/ba6d113f166bfb4cf4dc470ad012f2ba/1000x1000-000000-80-0-0.jpg",
      "nb_album": 90,
      "nb_fan": 300594,
      "radio": true,
      "tracklist": "https://api.deezer.com/artist/10611/top?limit=50",
      "time_add": 1533561236,
      "type": "artist"
    },
    {
      "id": "246791",
      "name": "Drake",
      "link": "https://www.deezer.com/artist/246791",
      "picture": "https://api.deezer.com/artist/246791/image",
      "picture_small": "https://e-cdns-images.dzcdn.net/images/artist/5d2fa7f140a6bdc2c864c3465a61fc71/56x56-000000-80-0-0.jpg",
      "picture_medium": "https://e-cdns-images.dzcdn.net/images/artist/5d2fa7f140a6bdc2c864c3465a61fc71/250x250-000000-80-0-0.jpg",
      "picture_big": "https://e-cdns-images.dzcdn.net/images/artist/5d2fa7f140a6bdc2c864c3465a61fc71/500x500-000000-80-0-0.jpg",
      "picture_xl": "https://e-cdns-images.dzcdn.net/images/artist/5d2fa7f140a6bdc2c864c3465a61fc71/1000x1000-000000-80-0-0.jpg",
      "nb_album": 39,
      "nb_fan": 16014203,
      "radio": true,
      "tracklist": "https://api.deezer.com/artist/246791/top?limit=50",
      "time_add": 1533561244,
      "type": "artist"
    },
    {
      "id": "4417245",
      "name": "Leon Vynehall",
      "link": "https://www.deezer.com/artist/4417245",
      "picture": "https://api.deezer.com/artist/4417245/image",
      "picture_small": "https://e-cdns-images.dzcdn.net/images/artist/735eaf92113cc8496cfe37942f394444/56x56-000000-80-0-0.jpg",
      "picture_medium": "https://e-cdns-images.dzcdn.net/images/artist/735eaf92113cc8496cfe37942f394444/250x250-000000-80-0-0.jpg",
      "picture_big": "https://e-cdns-images.dzcdn.net/images/artist/735eaf92113cc8496cfe37942f394444/500x500-000000-80-0-0.jpg",
      "picture_xl": "https://e-cdns-images.dzcdn.net/images/artist/735eaf92113cc8496cfe37942f394444/1000x1000-000000-80-0-0.jpg",
      "nb_album": 12,
      "nb_fan": 5318,
      "radio": true,
      "tracklist": "https://api.deezer.com/artist/4417245/top?limit=50",
      "time_add": 1533826695,
      "type": "artist"
    },
    {
      "id": "4495513",
      "name": "Travis Scott",
      "link": "https://www.deezer.com/artist/4495513",
      "picture": "https://api.deezer.com/artist/4495513/image",
      "picture_small": "https://e-cdns-images.dzcdn.net/images/artist/c1689f623450a7bf2e177b7564658a07/56x56-000000-80-0-0.jpg",
      "picture_medium": "https://e-cdns-images.dzcdn.net/images/artist/c1689f623450a7bf2e177b7564658a07/250x250-000000-80-0-0.jpg",
      "picture_big": "https://e-cdns-images.dzcdn.net/images/artist/c1689f623450a7bf2e177b7564658a07/500x500-000000-80-0-0.jpg",
      "picture_xl": "https://e-cdns-images.dzcdn.net/images/artist/c1689f623450a7bf2e177b7564658a07/1000x1000-000000-80-0-0.jpg",
      "nb_album": 23,
      "nb_fan": 303957,
      "radio": true,
      "tracklist": "https://api.deezer.com/artist/4495513/top?limit=50",
      "time_add": 1533826704,
      "type": "artist"
    },
    {
      "id": "9197980",
      "name": "Damso",
      "link": "https://www.deezer.com/artist/9197980",
      "picture": "https://api.deezer.com/artist/9197980/image",
      "picture_small": "https://e-cdns-images.dzcdn.net/images/artist/f1a596b126611260994271ce4cb54bb0/56x56-000000-80-0-0.jpg",
      "picture_medium": "https://e-cdns-images.dzcdn.net/images/artist/f1a596b126611260994271ce4cb54bb0/250x250-000000-80-0-0.jpg",
      "picture_big": "https://e-cdns-images.dzcdn.net/images/artist/f1a596b126611260994271ce4cb54bb0/500x500-000000-80-0-0.jpg",
      "picture_xl": "https://e-cdns-images.dzcdn.net/images/artist/f1a596b126611260994271ce4cb54bb0/1000x1000-000000-80-0-0.jpg",
      "nb_album": 10,
      "nb_fan": 1902918,
      "radio": true,
      "tracklist": "https://api.deezer.com/artist/9197980/top?limit=50",
      "time_add": 1533561241,
      "type": "artist"
    }
  ],
  "checksum": "1dc6e872e6f0ecbda9d88415a6cfea09",
  "total": 13
}
    '''

@pytest.fixture
def deezer_api_playlists_output():
    return '''
    {
  "data": [
    {
      "id": "4751468944",
      "title": "House",
      "duration": 0,
      "public": true,
      "is_loved_track": false,
      "collaborative": false,
      "rating": 0,
      "nb_tracks": 0,
      "fans": 0,
      "link": "https://www.deezer.com/playlist/4751468944",
      "picture": "https://api.deezer.com/playlist/4751468944/image",
      "picture_small": "https://e-cdns-images.dzcdn.net/images/cover//56x56-000000-80-0-0.jpg",
      "picture_medium": "https://e-cdns-images.dzcdn.net/images/cover//250x250-000000-80-0-0.jpg",
      "picture_big": "https://e-cdns-images.dzcdn.net/images/cover//500x500-000000-80-0-0.jpg",
      "picture_xl": "https://e-cdns-images.dzcdn.net/images/cover//1000x1000-000000-80-0-0.jpg",
      "checksum": "15d2b9ad8771abd4337e8fed2b96c3a1",
      "tracklist": "https://api.deezer.com/playlist/4751468944/tracks",
      "creation_date": "2018-08-09 15:00:21",
      "time_add": 1533826821,
      "time_mod": 1533826821,
      "creator": {
        "id": "2254154044",
        "name": "spins-music",
        "tracklist": "https://api.deezer.com/user/2254154044/flow",
        "type": "user"
      },
      "type": "playlist"
    },
    {
      "id": "4741928984",
      "title": "Loved Tracks",
      "duration": 756,
      "public": true,
      "is_loved_track": true,
      "collaborative": false,
      "rating": 0,
      "nb_tracks": 3,
      "fans": 0,
      "link": "https://www.deezer.com/playlist/4741928984",
      "picture": "https://api.deezer.com/playlist/4741928984/image",
      "picture_small": "https://e-cdns-images.dzcdn.net/images/playlist/f0604f1104723a8cb0bd1439bc6f6a30/56x56-000000-80-0-0.jpg",
      "picture_medium": "https://e-cdns-images.dzcdn.net/images/playlist/f0604f1104723a8cb0bd1439bc6f6a30/250x250-000000-80-0-0.jpg",
      "picture_big": "https://e-cdns-images.dzcdn.net/images/playlist/f0604f1104723a8cb0bd1439bc6f6a30/500x500-000000-80-0-0.jpg",
      "picture_xl": "https://e-cdns-images.dzcdn.net/images/playlist/f0604f1104723a8cb0bd1439bc6f6a30/1000x1000-000000-80-0-0.jpg",
      "checksum": "2ccb9c18caef7d4f1fd7b1bc746d8a54",
      "tracklist": "https://api.deezer.com/playlist/4741928984/tracks",
      "creation_date": "2018-08-06 13:13:09",
      "time_add": 1533826804,
      "time_mod": 1533826804,
      "creator": {
        "id": "2254154044",
        "name": "spins-music",
        "tracklist": "https://api.deezer.com/user/2254154044/flow",
        "type": "user"
      },
      "type": "playlist"
    }
  ],
  "checksum": "a69b9aaded3e43fbf8cb7432ee67a84140cd750bba9870f18aada2478b24840a",
  "total": 2
}
    '''


def test_customization_service_parser_track(deezer_api_tracks_output):
    tracks = DeezerCustomizationService.parse_entity("tracks", deezer_api_tracks_output)
    assert len(tracks) == 3
    assert tracks[0].name == "SICKO MODE"

def test_customization_service_parser_track_empty():
    data = '''
    { 
        "data": [], 
        "checksum": "checksum", 
        "total": 0
    }      
    '''
    tracks = DeezerCustomizationService.parse_entity("tracks", data)
    assert len(tracks) == 0

def test_customization_service_parser_artist(deezer_api_artists_output):
    artists = DeezerCustomizationService.parse_entity("artists", deezer_api_artists_output)

    assert len(artists) == 13


def test_customization_service_parser_playlist(deezer_api_playlists_output):

    playlists = DeezerCustomizationService.parse_entity("playlists", deezer_api_playlists_output)
    assert len(playlists) == 1