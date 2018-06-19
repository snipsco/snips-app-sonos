from snipssonos.services.spotify.music_search_service import SpotifyMusicSearchService
from tests.services.spotify.raw_responses import *


# Testing Music Search Service
def test_music_service_empty_song_name():
    pass


# Testing Spotify Music Service
def test_correct_parsing_of_tracks_for_correct_response():
    client = SpotifyMusicSearchService("client_id", "client_secret")
    tracks = client._parse_track_results(TRACKS)

    assert len(tracks) == 20
    assert tracks[0].uri == "spotify:track:3f9HJzevC4sMYGDwj7yQwd"


def test_correct_parsing_of_tracks_with_empty_response():
    client = SpotifyMusicSearchService("client_id", "client_secret")
    tracks = client._parse_track_results(EMPTY_TRACKS)

    assert len(tracks) == 0


def test_correct_parsing_of_playlists_for_correct_response():
    client = SpotifyMusicSearchService("client_id", "client_secret")
    playlists = client._parse_playlist_results(PLAYLISTS)

    assert len(playlists) == 20
    assert playlists[0].name == "Peaceful Piano"
    assert playlists[0].uri == "spotify:user:spotify:playlist:37i9dQZF1DX4sWSpwq3LiO"


def test_correct_parsing_of_artists_for_correct_response():
    client = SpotifyMusicSearchService("client_id", "client_secret")
    artists = client._parse_artists_results(ARTISTS)

    assert len(artists) == 1
    assert artists[0].name == "Tornado Wallace"
    assert artists[0].uri == "spotify:artist:6GNWPphcJ5CtIwCJVV1lLT"


def test_correct_parsing_of_albums_for_correct_response():
    client = SpotifyMusicSearchService("client_id", "client_secret")
    artists = client._parse_album_results(ALBUMS)

    assert len(artists) == 2
    assert artists[0].name == "KIDS SEE GHOSTS"
    assert artists[0].uri == "spotify:album:6pwuKxMUkNg673KETsXPUV"
