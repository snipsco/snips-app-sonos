import pytest

from snipssonos.use_cases import request_objects as reqo


def test_build_play_music_request_object_from_empty_dict():
    play_track_request = reqo.PlayMusicRequestFactory.from_dict(dict())

    assert bool(play_track_request) is True


def test_build_play_music_request_object_from_artist():
    adict = {
        'artist_name': 'Nekfeu'
    }

    play_music_request = reqo.PlayMusicRequestFactory.from_dict(adict)

    assert bool(play_music_request) is True


def test_build_play_track_request_object_from_track():
    adict = {
        'track_name': 'Mauvaise Graine'
    }

    play_music_request = reqo.PlayMusicRequestFactory.from_dict(adict)

    assert bool(play_music_request) is True


def test_build_play_track_request_object_from_album():
    adict = {
        'album_name': 'Feu'
    }

    play_music_request = reqo.PlayMusicRequestFactory.from_dict(adict)

    assert bool(play_music_request) is True


def test_build_play_track_request_object_from_artist_and_track():
    adict = {
        'artist_name': 'Nekfeu',
        'album_name': 'Feu',
    }

    play_music_request = reqo.PlayMusicRequestFactory.from_dict(adict)

    assert bool(play_music_request) is True
