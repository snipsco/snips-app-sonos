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
        self.client.set_top_artist()
        artists_results = []
        for time_range in self.TIME_RANGES:
            top_artist_by_time_range_query = SpotifyAPISearchQueryBuilder()
            top_artist_by_time_range_query = top_artist_by_time_range_query\
                .add_time_range(time_range)
                # .add_limit(50)

            raw_response = self.client.execute_query(None) # TODO fix query builder
            artists = self.parse_artist_results(raw_response)
            artists_results.append(artists)

        return artists_results

    # def fetch_top_tracks(self, time_range=None):
    # def fetch_playlist(self):

    @staticmethod
    def parse_artist_results(raw_response):
        response = json.loads(raw_response)
        artists = [Artist(item['name']) for item in response['items']]

        return artists


# TODO erase, just testing purposes
if __name__ == "__main__":
    client_id = ""
    client_secret = ""
    access_token = ""

    custom = SpotifyCustomService(client_id, client_secret, access_token)

    results_artist = custom.fetch_top_artist()
    print(results_artist)
