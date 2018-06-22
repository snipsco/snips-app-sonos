import json

from snipssonos.entities.artist import Artist
from snipssonos.entities.track import Track
from snipssonos.entities.playlist import Playlist
from snipssonos.helpers.spotify_client import SpotifyClient, SpotifyAPISearchQueryBuilder


class SpotifyCustomizationService:
    TIME_RANGES = ["long_term", "medium_term", "short_term"]

    def __init__(self, client_id, client_secret, access_token=None, refresh_token=None):
        self.client = SpotifyClient(client_id, client_secret, access_token, refresh_token)
        self.client_id = client_id
        self.client_secret = client_secret

    def fetch_entity(self, entity_type):
        entity_results = []

        if entity_type == "playlists":
            top_entity_type_query = SpotifyAPISearchQueryBuilder() \
                .set_user_query(entity_type) \
                .add_limit(50)

            entity_results += self.execute_and_parse_query(entity_type, top_entity_type_query)
        else:
            for time_range in self.TIME_RANGES:
                top_entity_type_by_time_range_query = SpotifyAPISearchQueryBuilder() \
                    .set_user_query(entity_type) \
                    .add_time_range(time_range)\
                    .add_limit(50)

                entity_results += self.execute_and_parse_query(entity_type,
                                                               top_entity_type_by_time_range_query)
        return entity_results

    def execute_and_parse_query(self, entity_type, query):
        raw_response = self.client.execute_query(query)
        return self.parse_results(entity_type, raw_response)

    @staticmethod
    def parse_results(entity_type, raw_response):
        if entity_type == "artists":
            response = json.loads(raw_response)
            artists = [Artist(item['uri'], item['name']) for item in response['items']]
            return artists

        elif entity_type == "tracks":
            response = json.loads(raw_response)
            tracks = [Track(item['uri'], item['name']) for item in response['items']]
            return tracks

        elif entity_type == "playlists":
            response = json.loads(raw_response)
            playlists = [Playlist(item['uri'], item['name']) for item in response['items']]
            return playlists
