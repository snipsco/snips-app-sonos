import json

from snipssonos.services.spotify.music_search_service import SpotifyMusicSearchService
from tests.services.spotify.raw_responses import *
from snipssonos.entities.artist import Artist


# Testing Spotify Music Service
def test_correct_parsing_of_tracks_for_correct_response():
    client = SpotifyMusicSearchService("client_id", "client_secret", "refresh_token")
    tracks = client._parse_track_results(TRACKS)

    artists = tracks[0].artists

    assert len(tracks) == 20
    assert tracks[0].uri == "spotify:track:3f9HJzevC4sMYGDwj7yQwd"
    assert tracks[0].name == "April the 14th Part 1"
    assert artists[0].name == "Gillian Welch"


def test_correct_parsing_of_tracks_with_empty_response():
    client = SpotifyMusicSearchService("client_id", "client_secret", "refresh_token")
    tracks = client._parse_track_results(EMPTY_TRACKS)

    assert len(tracks) == 0


def test_correct_parsing_of_playlists_for_correct_response():
    client = SpotifyMusicSearchService("client_id", "client_secret", "refresh_token")
    playlists = client._parse_playlist_results(PLAYLISTS)

    assert len(playlists) == 20
    assert playlists[0].name == "Peaceful Piano"
    assert playlists[0].uri == "spotify:user:spotify:playlist:37i9dQZF1DX4sWSpwq3LiO"


def test_correct_parsing_of_artists_for_correct_response():
    client = SpotifyMusicSearchService("client_id", "client_secret", "refresh_token")
    artists = client._parse_artists_results(ARTISTS)

    assert len(artists) == 1
    assert artists[0].name == "Tornado Wallace"
    assert artists[0].uri == "spotify:artist:6GNWPphcJ5CtIwCJVV1lLT"


def test_correct_parsing_of_albums_for_correct_response():
    client = SpotifyMusicSearchService("client_id", "client_secret", "refresh_token")
    albums = client._parse_album_results(ALBUMS)

    artists = albums[0].artists

    assert len(albums) == 2
    assert albums[0].name == "KIDS SEE GHOSTS"
    assert albums[0].uri == "spotify:album:6pwuKxMUkNg673KETsXPUV"
    assert artists[0].name == "KIDS SEE GHOSTS"
    assert artists[1].name == "Kanye West"
    assert artists[2].name == "Kid Cudi"


def test_get_artists_from_album():
    client = SpotifyMusicSearchService("client_id", "client_secret", "refresh_token")
    response = json.loads(ALBUMS)
    albums = response['albums']

    artists = client._get_artists_from_item(albums['items'][0])

    assert isinstance(artists[0], Artist)
    assert isinstance(artists[1], Artist)
    assert isinstance(artists[2], Artist)

    # artists_name == "KIDS SEE GHOSTS, Kanye West, Kid Cudi"
