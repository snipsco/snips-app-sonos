import base64
import logging
import requests
import time

from snipssonos.exceptions import MusicSearchProviderConnectionError, MusicSearchCredentialsError, \
    SpotifyQueryBuilderNonExistentTimeRange, SpotifyClientAuthorizationException, \
    SpotifyClientAuthRefreshAccessTokenException


class SpotifyClient(object):
    """
    This class contains helper methods to request the Spotify Web API.
    It covers all endpoints of the API, but most helpers functions are for authentication.

    Please refer to the Authorization Code Flow section on this page : https://developer.spotify.com/documentation/general/guides/authorization-guide/
    """
    AUTH_SERVICE_ENDPOINT = "https://accounts.spotify.com/api/token"

    def __init__(self, client_id, client_secret, refresh_token=None):
        self.client_id = str(client_id)
        self.client_secret = str(client_secret)
        self.refresh_token = refresh_token
        self.access_token = None
        self.access_token_expiration = None
        self.endpoint = None

        self._check_credentials_validity()

    def request_access_and_refresh_tokens(self, authorization_code, host_redirect_uri):
        """
        This method is called when making a first authentication with the Spotify We API.

        """
        if authorization_code is None:
            logging.error("No authorization was provided to the SpotifyClient. Cannot pursue authentication process.")
            raise SpotifyClientAuthorizationException("No Authorization code was provided.")
        try:
            logging.debug("An authorization code was retrieved. Now requesting refresh and access tokens from Spotify.")
            headers = self._get_authorization_headers_from_client_credentials()
            response = requests.post(
                self.AUTH_SERVICE_ENDPOINT,
                headers=headers,
                data={
                    'grant_type': 'authorization_code',
                    'code': authorization_code,
                    'redirect_uri': host_redirect_uri
                }
            )

            if response.ok:
                logging.debug("Succesfully retrieved the refresh and access tokens.")

                access_token = self._extract_access_token(response)
                refresh_token = self._extract_refresh_token(response)
                expires_in = self._extract_access_token_expiration(response)
                return access_token, refresh_token, expires_in
            else:
                logging.error(
                    "We successfully retrieved the authorization code, but something happened while requesting refresh token and access token")
                raise SpotifyClientAuthRefreshAccessTokenException(
                    "We successfully retrieved the authorization code, but something happened while requesting refresh token and access token")

        except requests.exceptions.ConnectionError as e:
            raise MusicSearchProviderConnectionError(
                "Connection error, could not connnect to Spotify Services : {}".format(e.message))

    def _check_credentials_validity(self):
        if not (len(self.client_id) * len(self.client_secret)):
            raise MusicSearchCredentialsError("Could not find client_id or client_secret")

    def _get_base_64_encoded_credentials(self):
        credentials_string = "{}:{}".format(self.client_id, self.client_secret)
        base64_encoded_credentials = base64.b64encode(credentials_string)
        return base64_encoded_credentials

    def _extract_access_token(self, response):
        return response.json()['access_token']

    def _extract_refresh_token(self, response):
        return response.json()['refresh_token']

    def _extract_access_token_expiration(self, response):
        return response.json()['expires_in']

    def _set_access_token_expiration_time(self, response):
        expires_in = self._extract_access_token_expiration(response)
        self.access_token_expiration = time.time() + expires_in

    def _get_authorization_headers_from_client_credentials(self):
        base64_encoded_credentials = self._get_base_64_encoded_credentials()
        auth_headers = {'Authorization': 'Basic {}'.format(base64_encoded_credentials)}
        return auth_headers

    def _get_authorization_headers_from_access_token(self):
        if not len(self.access_token):
            raise MusicSearchCredentialsError("No access token found")
        else:
            auth_headers = {'Authorization': 'Bearer {}'.format(self.access_token)}
            return auth_headers

    def retrieve_access_token(self):
        try:

            headers = self._get_authorization_headers_from_client_credentials()
            response = requests.post(
                self.AUTH_SERVICE_ENDPOINT,
                headers=headers,
                data={
                    'grant_type': 'refresh_token',  # This is problematic for me here ....
                    'refresh_token': self.refresh_token
                }
            )
            access_token = self._extract_access_token(response)
            self._set_access_token_expiration_time(response)
            return access_token

        except requests.exceptions.ConnectionError as e:
            raise MusicSearchProviderConnectionError(
                "There was a problem retrieving the access token: {}".format(e.message))

    def authenticate(self):
        """
        This method assumes that you already requested an acces and refresh token with the request_access_and_refresh_token method.
        This method is used to refresh the access token when you already have a valid refresh token.
        """
        if self.access_token is None or time.time() > self.access_token_expiration:
            self.access_token = self.retrieve_access_token()

    def execute_query(self, query):
        try:
            self.authenticate()
            headers = self._get_authorization_headers_from_access_token()
            response = requests.get(
                query.endpoint,
                params=query.params_to_dict(),
                headers=headers)
            if response.ok:
                return response.text
            else:
                raise MusicSearchProviderConnectionError(
                    "There was a problem while making a request to Spotify: '{} with status code {}',"
                    " while hitting the endpoint {}"
                        .format(response.reason, response.status_code, query.endpoint))
        except requests.exceptions.ConnectionError as e:
            raise MusicSearchProviderConnectionError(
                "There was a problem while querying to Spotify api: {}".format(e.message))


class SpotifyAPISearchQueryBuilder(object):
    ENTITY_TYPES = ["artists", "tracks", "playlists"]
    TIME_RANGES = ["long_term", "medium_term", "short_term"]

    SPOTIFY_ENDPOINT = "https://api.spotify.com/v1"
    SEARCH_QUERY = 'search'
    USER_QUERY = 'me'

    def __init__(self):
        self.keyword = ""
        self.field_filters = []
        self.user_filters = {}
        self.result_type = None
        self.endpoint = None

    def set_search_query(self):
        self.endpoint = "{}/{}".format(self.SPOTIFY_ENDPOINT, self.SEARCH_QUERY)
        return self

    def set_user_query(self, entity_name=None):
        self.endpoint = "{}/{}".format(self.SPOTIFY_ENDPOINT, self.USER_QUERY)
        if entity_name in self.ENTITY_TYPES:
            return self.with_playlists() if entity_name == "playlists" else \
                getattr(self, "with_top_{}".format(entity_name))()
        return self

    def with_top_artists(self):
        self.endpoint = "{}/top/artists".format(self.endpoint)
        return self

    def with_top_tracks(self):
        self.endpoint = "{}/top/tracks".format(self.endpoint)
        return self

    def with_playlists(self):
        self.endpoint = "{}/playlists".format(self.endpoint)
        return self

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
        self.is_valid_time_range(time_range)
        self.user_filters.update({'time_range': time_range})
        return self

    def add_limit(self, limit):
        self.user_filters.update({'limit': limit})
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
        return u''.join([u"{}:{} ".format(field_filter[0], field_filter[1]) for field_filter in
                        self.field_filters]).strip()

    def params_to_dict(self):
        params_dictionary = {}
        if self.is_user_query_set():
            params_dictionary = self.user_filters
        else:
            if len(self.field_filters):
                query = self._get_query_from_field_filters()
                params_dictionary.update({'q': query})
            else:
                query = self.keyword
                params_dictionary.update({'q': query})

            if self.result_type:
                params_dictionary.update({'type': self.result_type})

        return params_dictionary

    def is_valid_time_range(self, time_range):
        if time_range not in self.TIME_RANGES:
            raise SpotifyQueryBuilderNonExistentTimeRange("The time range {} is not defined".format(time_range))

    def is_user_query_set(self):
        if self.endpoint is not None and "me" in self.endpoint:
            return True
        return False
