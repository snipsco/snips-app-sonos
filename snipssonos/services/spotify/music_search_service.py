import json


from snipssonos.entities.track import Track
from snipssonos.entities.album import Album
from snipssonos.entities.artist import Artist
from snipssonos.entities.playlist import Playlist
from snipssonos.services.music.search_service import MusicSearchService
from snipssonos.helpers.spotify_client import SpotifyClient, SpotifyAPISearchQueryBuilder


class SpotifyMusicSearchService(MusicSearchService):
    def __init__(self, client_id, client_secret, refresh_token):
        self.client = SpotifyClient(client_id, client_secret, refresh_token)
        self.client_id = client_id
        self.client_secret = client_secret

    def search_album(self, album_name):
        album_search_query = SpotifyAPISearchQueryBuilder() \
            .set_search_query() \
            .add_album_result_type() \
            .add_generic_search_term(album_name)

        raw_response = self.client.execute_query(album_search_query)
        albums = self._parse_album_results(raw_response)
        return albums

    def search_album_in_playlist(self, album_name, playlist_name):
        album_search_query = SpotifyAPISearchQueryBuilder() \
            .set_search_query() \
            .add_album_result_type() \
            .add_album_filter(album_name) \
            .add_playlist_filter(playlist_name)

        raw_response = self.client.execute_query(album_search_query)
        albums = self._parse_album_results(raw_response)
        return albums

    def search_album_for_artist(self, album_name, artist_name):
        album_search_query = SpotifyAPISearchQueryBuilder() \
            .set_search_query() \
            .add_album_result_type() \
            .add_album_filter(album_name) \
            .add_artist_filter(artist_name)

        raw_response = self.client.execute_query(album_search_query)
        albums = self._parse_album_results(raw_response)
        return albums

    def search_album_for_artist_and_for_playlist(self, album_name, artist_name, playlist_name):
        album_search_query = SpotifyAPISearchQueryBuilder() \
            .set_search_query() \
            .add_album_result_type() \
            .add_album_filter(album_name) \
            .add_artist_filter(artist_name) \
            .add_playlist_filter(playlist_name)

        raw_response = self.client.execute_query(album_search_query)
        albums = self._parse_album_results(raw_response)
        return albums

    def search_track(self, track_name):
        song_search_query = SpotifyAPISearchQueryBuilder() \
            .set_search_query() \
            .add_track_result_type() \
            .add_generic_search_term(track_name)

        raw_response = self.client.execute_query(song_search_query)
        tracks = self._parse_track_results(raw_response)
        return tracks

    def search_track_for_artist(self, track_name, artist_name):
        track_by_artist_search_query = SpotifyAPISearchQueryBuilder() \
            .set_search_query() \
            .add_track_result_type() \
            .add_artist_filter(artist_name) \
            .add_track_filter(track_name)

        raw_response = self.client.execute_query(track_by_artist_search_query)
        tracks = self._parse_track_results(raw_response)
        return tracks

    def search_track_for_album(self, track_name, album_name):
        track_by_album_search_query = SpotifyAPISearchQueryBuilder() \
            .set_search_query() \
            .add_track_filter(track_name) \
            .add_album_filter(album_name)

        raw_response = self.client.execute_query(track_by_album_search_query)
        tracks = self._parse_track_results(raw_response)
        return tracks

    def search_track_for_playlist(self, track_name, playlist_name):
        track_by_playlist_search_query = SpotifyAPISearchQueryBuilder() \
            .set_search_query() \
            .add_track_filter(track_name) \
            .add_playlist_filter(playlist_name)

        raw_response = self.client.execute_query(track_by_playlist_search_query)
        tracks = self._parse_track_results(raw_response)
        return tracks

    def search_track_for_album_and_for_artist(self, track_name, album_name, artist_name):
        track_by_album_and_artist_search_query = SpotifyAPISearchQueryBuilder() \
            .set_search_query() \
            .add_track_result_type() \
            .add_album_filter(album_name) \
            .add_artist_filter(artist_name) \
            .add_track_filter(track_name)

        raw_response = self.client.execute_query(track_by_album_and_artist_search_query)
        tracks = self._parse_track_results(raw_response)
        return tracks

    def search_track_for_album_and_for_playlist(self, track_name, album_name, playlist_name):
        track_by_album_and_playlist_search_query = SpotifyAPISearchQueryBuilder() \
            .set_search_query() \
            .add_track_result_type() \
            .add_album_filter(album_name) \
            .add_playlist_filter(playlist_name) \
            .add_track_filter(track_name)

        raw_response = self.client.execute_query(track_by_album_and_playlist_search_query)
        tracks = self._parse_track_results(raw_response)
        return tracks

    def search_track_for_artist_and_for_playlist(self, track_name, artist_name, playlist_name):
        track_by_artist_and_playlist_search_query = SpotifyAPISearchQueryBuilder() \
            .set_search_query() \
            .add_track_result_type() \
            .add_artist_filter(artist_name) \
            .add_playlist_filter(playlist_name) \
            .add_track_filter(track_name)

        raw_response = self.client.execute_query(track_by_artist_and_playlist_search_query)
        tracks = self._parse_track_results(raw_response)
        return tracks

    def search_track_for_album_and_for_artist_and_for_playlist(self, track_name, album_name, artist_name,
                                                               playlist_name):
        track_by_album_and_artist_and_playlist_search_query = SpotifyAPISearchQueryBuilder() \
            .set_search_query() \
            .add_track_result_type() \
            .add_album_filter(album_name) \
            .add_artist_filter(artist_name) \
            .add_playlist_filter(playlist_name) \
            .add_track_filter(track_name)

        raw_response = self.client.execute_query(track_by_album_and_artist_and_playlist_search_query)
        tracks = self._parse_track_results(raw_response)
        return tracks

    def search_artist(self, artist_name):
        artist_search_query = SpotifyAPISearchQueryBuilder() \
            .set_search_query() \
            .add_track_result_type() \
            .add_artist_filter(artist_name)

        raw_response = self.client.execute_query(artist_search_query)
        tracks_by_artist = self._parse_track_results(raw_response)
        return tracks_by_artist

    def search_artist_for_playlist(self, artist_name, playlist_name):
        track_by_artist_in_playlist_search_query = SpotifyAPISearchQueryBuilder() \
            .set_search_query() \
            .add_artist_result_type() \
            .add_field_filter("artist", artist_name) \
            .add_field_filter("playlist", playlist_name)

        raw_response = self.client.execute_query(track_by_artist_in_playlist_search_query)
        artists = self._parse_artists_results(raw_response)

        return artists

    def search_playlist(self, playlist_name):
        playlist_search_query = SpotifyAPISearchQueryBuilder() \
            .set_search_query() \
            .add_playlist_result_type() \
            .add_generic_search_term(playlist_name)

        raw_response = self.client.execute_query(playlist_search_query)
        playlists = self._parse_playlist_results(raw_response)

        return playlists

    def _parse_track_results(self, raw_response):
        response = json.loads(raw_response)
        tracks = response['tracks']

        tracks = [Track(item['uri']) for item in tracks['items']]

        return tracks

    def _parse_playlist_results(self, raw_response):
        response = json.loads(raw_response)
        playlists = response['playlists']

        playlists = [Playlist(item['uri'], item['name']) for item in playlists['items']]
        return playlists

    def _parse_artists_results(self, raw_response):
        response = json.loads(raw_response)
        artists = response['artists']

        artists = [Artist(item['uri'], item['name']) for item in artists['items']]
        return artists

    def _parse_album_results(self, raw_response):
        response = json.loads(raw_response)
        albums = response['albums']

        artists = [Album(item['uri'], item['name']) for item in albums['items']]
        return artists



