import json

from snipssonos.entities.artist import Artist
from snipssonos.helpers.spotify_client import SpotifyClient, SpotifyAPISearchQueryBuilder


class SpotifyCustomService:
    TIME_RANGES = ["long_term", "medium_term", "short_term"]

    def __init__(self, client_id, client_secret, access_token=None, refresh_token=None):
        self.client = SpotifyClient(client_id, client_secret, access_token, refresh_token)
        self.client_id = client_id
        self.client_secret = client_secret

        self.client.set_user_endpoint()

    def fetch_top_artist(self):
        self.client.set_top_artist_endpoint()
        artists_results = []
        for time_range in self.TIME_RANGES:
            top_artist_by_time_range_query = SpotifyAPISearchQueryBuilder(is_request_user_data_query=True)
            top_artist_by_time_range_query = top_artist_by_time_range_query\
                .add_time_range(time_range)\
                .add_limit(50)

            raw_response = self.client.execute_query(top_artist_by_time_range_query)
            artists_results += self.parse_artist_results(raw_response)
        return artists_results

    def reset_user_endpoint(self):
        self.client.set_user_endpoint()

    @staticmethod
    def parse_artist_results(raw_response):
        response = json.loads(raw_response)
        artists = [Artist(item['uri'], item['name']) for item in response['items']]

        return artists
