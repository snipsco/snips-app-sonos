import json

from snipssonos.entities.artist import Artist
from snipssonos.helpers.spotify_client import SpotifyClient, SpotifyAPISearchQueryBuilder


class SpotifyCustomizationService:
    TIME_RANGES = ["long_term", "medium_term", "short_term"]

    def __init__(self, client_id, client_secret, access_token=None, refresh_token=None):
        self.client = SpotifyClient(client_id, client_secret, access_token, refresh_token)
        self.client_id = client_id
        self.client_secret = client_secret

    def fetch_top_artist(self):
        artists_results = []
        for time_range in self.TIME_RANGES:
            top_artist_by_time_range_query = SpotifyAPISearchQueryBuilder() \
                .set_user_query() \
                .with_top_artists() \
                .add_time_range(time_range)\
                .add_limit(50)

            raw_response = self.client.execute_query(top_artist_by_time_range_query)
            artists_results += self.parse_artist_results(raw_response)
        return artists_results

    @staticmethod
    def parse_artist_results(raw_response):
        response = json.loads(raw_response)
        artists = [Artist(item['uri'], item['name']) for item in response['items']]

        return artists
