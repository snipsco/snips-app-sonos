import pytest

from snipssonos.use_cases import request_objects as reqo


def test_build_play_track_request_object_from_empty_dict():
    play_track_request = reqo.PlayMusicRequestObject.from_dict(dict())

    assert bool(play_track_request) is False


def test_build_play_track_request_object_from_artist():
    adict = {
        'music_items': [
            {
                'name': 'Nekfeu',
                'type': 'artist'
            }
        ]
    }

    play_track_request = reqo.PlayMusicRequestObject.from_dict(adict)

    assert bool(play_track_request) is True
    assert isinstance(play_track_request.music_items[0], reqo.PlayMusicRequestObject.ArtistItem)


def test_build_play_track_request_object_from_track():
    adict = {
        'music_items': [
            {
                'name': 'Mauvaise Graine',
                'type': 'track'
            }
        ]
    }

    play_track_request = reqo.PlayMusicRequestObject.from_dict(adict)

    assert bool(play_track_request) is True
    assert isinstance(play_track_request.music_items[0], reqo.PlayMusicRequestObject.TrackItem)


def test_build_play_track_request_object_from_album():
    adict = {
        'music_items': [
            {
                'name': 'Feu',
                'type': 'album'
            }
        ]
    }

    play_track_request = reqo.PlayMusicRequestObject.from_dict(adict)

    assert bool(play_track_request) is True
    assert isinstance(play_track_request.music_items[0], reqo.PlayMusicRequestObject.AlbumItem)


def test_build_play_track_request_object_from_artist_and_track():
    adict = {
        'music_items': [
            {
                'name': 'Nekfeu',
                'type': 'artist'
            },
            {
                'name': 'Feu',
                'type': 'album'
            }
        ]
    }

    play_track_request = reqo.PlayMusicRequestObject.from_dict(adict)

    assert bool(play_track_request) is True
    assert len(play_track_request.music_items) == 2
