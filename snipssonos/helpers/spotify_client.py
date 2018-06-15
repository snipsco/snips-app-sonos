import base64
import requests

from snipssonos.exceptions import MusicSearchProviderConnectionError, MusicSearchCredentialsError


class SpotifyClient(object):
    AUTH_SERVICE_ENDPOINT = "https://accounts.spotify.com/api/token"
    SEARCH_ENDPOINT = "https://api.spotify.com/v1/search"
    USER_ENDPOINT = "https://api.spotify.com/v1/me"

    def __init__(self, client_id, client_secret, access_token=None, refresh_token=None):
        self.client_id = str(client_id)
        self.client_secret = str(client_secret)
        self.refresh_token = refresh_token
        self.access_token = access_token
        self.endpoint = None

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

            # TODO figure what is going with this call
            # data = {
            #     'grant_type': 'refresh_token',
            #     'refresh_token': self.refresh_token
            # }
            access_token = self._extract_access_token(response)
            return access_token

        except requests.exceptions.ConnectionError as e:
            raise MusicSearchProviderConnectionError

    def authenticate(self):
        if self.access_token is None:
            self.access_token = self.retrieve_access_token()

    def execute_query(self, query=None):
        try:
            if query is not None:
                query = query.to_dict()
            self.authenticate()
            headers = self._get_authorization_headers_from_access_token()
            response = requests.get(
                self.endpoint,
                params=query,
                headers=headers)
            if response.ok:
                return response.text
            else:
                raise MusicSearchProviderConnectionError
        except requests.exceptions.ConnectionError as e:
            raise MusicSearchProviderConnectionError

    def set_search_endpoint(self):
            self.endpoint = self.SEARCH_ENDPOINT

    def set_user_endpoint(self, ):
        self.endpoint = self.USER_ENDPOINT
        return self

    def set_top_tracks(self):
        self.endpoint = "{}/top/{}".format(self.endpoint, "tracks")

    def set_top_artist(self):
        self.endpoint = "{}/top/{}".format(self.endpoint, "artists")

    def set_playlist(self):
        self.endpoint = "{}/{}".format(self.endpoint, "playlists")


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

    def add_playlist_filter(self, album_name):
        self.add_field_filter("playlist", album_name)
        return self

    def add_result_type(self, result_type):
        self.result_type = result_type
        return self

    def add_time_range(self, time_range):
        """
        Over what time frame the affinities are computed.
        :param time_range: long_term (last 4 years), medium_term (last 6 months) or short_term (last 4 weeks)
        :return:
        """
        self.add_field_filter("time_range", time_range)
        return self

    def add_limit(self, limit):
        self.add_field_filter("limit", limit)
        return self

    def add_track_result_type(self):
        return self.add_result_type("track")

    def add_playlist_result_type(self):
        return self.add_result_type("playlist")

    def add_artist_result_type(self):
        return self.add_result_type("artist")

    def add_album_result_type(self):
        return self.add_result_type("album")

    def add_field_filter(self, music_field_key, music_field_value):
        self.field_filters.append((music_field_key, music_field_value))
        return self

    def _get_query_from_field_filters(self):
        return ''.join(["{}:{} ".format(field_filter[0], field_filter[1]) for field_filter in
                        self.field_filters]).strip()

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
