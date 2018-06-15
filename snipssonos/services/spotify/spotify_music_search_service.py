import json


from snipssonos.entities.track import Track
from snipssonos.services.music.music_search_service import MusicSearchService
from snipssonos.helpers.spotify_client import SpotifyClient, SpotifyAPISearchQueryBuilder


class SpotifyMusicSearchService(MusicSearchService):
    def __init__(self, client_id, client_secret):
        self.client = SpotifyClient(client_id, client_secret)
        self.client_id = client_id
        self.client_secret = client_secret

        self.client = SpotifyClient(self.client_id, self.client_secret)
        self.client.set_search_endpoint()

    def search_track(self, song_name):
        song_search_query = SpotifyAPISearchQueryBuilder()\
            .add_track_result_type() \
            .add_generic_search_term(song_name)

        raw_response = self.client.execute_query(song_search_query)
        tracks = self._parse_track_results(raw_response)
        return tracks

    def search_track_for_artist(self, artist_name, track_name=None):
        track_by_artist_search_query = SpotifyAPISearchQueryBuilder()\
            .add_track_result_type()\
            .add_field_filter("artist", artist_name)

        if track_name:
            track_by_artist_search_query.add_track_filter(track_name)

        raw_response = self.client.execute_query(track_by_artist_search_query)
        tracks = self._parse_track_results(raw_response)
        return tracks

    @staticmethod
    def _parse_track_results(raw_response):
        response = json.loads(raw_response)
        tracks = response['tracks']

        tracks = [Track(item['uri']) for item in tracks['items']]

        return tracks



