import base64
import json
import requests

from snipssonos.entities.track import Track
from snipssonos.exceptions import MusicSearchProviderConnectionError, MusicSearchCredentialsError
from snipssonos.services.music_search_service import MusicSearchService


class SpotifyMusicSearchService(MusicSearchService):
    def __init__(self, client_id, client_secret):
        self.client = SpotifyClient(client_id, client_secret)
        self.client_id = client_id
        self.client_secret = client_secret

        self.client = SpotifyClient(self.client_id, self.client_secret)

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

    def _parse_track_results(self, raw_response):
        response = json.loads(raw_response)
        tracks = response['tracks']

        tracks = [Track(item['uri']) for item in tracks['items']]

        return tracks


class SpotifyClient(object):

    AUTH_SERVICE_ENDPOINT = "https://accounts.spotify.com/api/token"
    SEARCH_ENDPOINT = "https://api.spotify.com/v1/search"

    def __init__(self, client_id, client_secret):
        self.client_id = str(client_id)
        self.client_secret = str(client_secret)
        self.access_token = None

        self._check_credentials_validity()

    def _check_credentials_validity(self):
        if not (len(self.client_id) * len(self.client_secret)):
            raise MusicSearchCredentialsError

    def _get_base_64_encoded_credentials(self):
        credentials_string = "{}:{}".format(self.client_id, self.client_secret)
        base64_encoded_credentials = base64.b64encode(credentials_string)
        return base64_encoded_credentials

    def _extract_access_token(self, response):
        return response.json()['access_token']

    def _get_authorization_headers_from_client_credentials(self):
        base64_encoded_credentials = self._get_base_64_encoded_credentials()
        auth_headers = {'Authorization': 'Basic {}'.format(base64_encoded_credentials)}
        return auth_headers

    def _get_authorization_headers_from_access_token(self):
        if not len(self.access_token):
            raise MusicSearchCredentialsError
        else:
            auth_headers = {'Authorization': 'Bearer {}'.format(self.access_token)}
            return auth_headers

    def retrieve_access_token(self):
        try:

            headers = self._get_authorization_headers_from_client_credentials()

            response = requests.post(
                self.AUTH_SERVICE_ENDPOINT,
                headers=headers,
                data={'grant_type': 'client_credentials'}
            )
            access_token = self._extract_access_token(response)
            return access_token

        except requests.exceptions.ConnectionError as e:
            raise MusicSearchProviderConnectionError

    def authenticate(self):
        self.access_token = self.retrieve_access_token()

    def execute_query(self, query):
        try:
            self.authenticate()
            headers = self._get_authorization_headers_from_access_token()
            response = requests.get(
                self.SEARCH_ENDPOINT,
                params=query.to_dict(),
                headers=headers)
            if response.ok:
                return response.text
            else:
                raise MusicSearchProviderConnectionError
        except requests.exceptions.ConnectionError as e:
            raise MusicSearchProviderConnectionError


class SpotifyAPISearchQueryBuilder(object):
    def __init__(self):
        self.keyword = ""
        self.field_filters = []
        self.result_type = None

    def add_generic_search_term(self, term):
        if len(term):
            self.keyword = term
        return self

    def add_track_filter(self, track_name):
        self.add_field_filter("track", track_name)
        return self

    def add_artist_filter(self, artist_name):
        self.add_field_filter("artist", artist_name)
        return self

    def add_album_filter(self, album_name):
        self.add_field_filter("album", album_name)
        return self

    def add_result_type(self, result_type):
        self.result_type = result_type
        return self

    def add_track_result_type(self):
        self.add_result_type("track")
        return self

    def add_field_filter(self, music_field_key, music_field_value):
        self.field_filters.append((music_field_key, music_field_value))
        return self

    def _get_query_from_field_filters(self):
        return ''.join(["{}:{} ".format(field_filter[0], field_filter[1]) for field_filter in self.field_filters]).strip()

    def to_dict(self):
        params_dictionary = {}

        if len(self.field_filters):
            query = self._get_query_from_field_filters()
            params_dictionary.update({'q': query})
        else:
            query = self.keyword
            params_dictionary.update({'q': query})


        if self.result_type:
            params_dictionary.update({'type': self.result_type})

        return params_dictionary