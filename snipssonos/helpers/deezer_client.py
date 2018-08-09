import base64
import logging
import requests
import time

from snipssonos.exceptions import MusicSearchProviderConnectionError, MusicSearchCredentialsError, \
    DeezerClientAuthorizationException, DeezerClientAuthRefreshAccessTokenException, DeezerQueryBuilderException


class DeezerClient(object):
    """
    This class contains helper methods to request the Deezer Web API.
    It covers all endpoints of the API, but most helpers functions are for authentication.

    Please refer to the Authorization Code Flow section on this page : https://developers.deezer.com/api/oauth
    """
    AUTH_SERVICE_ENDPOINT = "https://connect.deezer.com/oauth/access_token.php"

    def __init__(self, app_id, secret, access_token=None):
        self.app_id = str(app_id)
        self.secret = str(secret)
        self.access_token = access_token
        self.access_token_expiration = None

        self._check_credentials_validity()

    def request_access_token(self, authorization_code):
        """
        This method is called when making a first authentication with the Deezer We API.

        """
        if authorization_code is None:
            logging.error("No authorization was provided to the DeezerClient. Cannot pursue authentication process.")
            raise DeezerClientAuthorizationException("No Authorization code was provided.")
        try:
            logging.debug("An authorization code was retrieved. Now requesting access token from Deezer.")

            response = requests.post(
                self.AUTH_SERVICE_ENDPOINT,
                data={
                    'app_id': self.app_id,
                    'secret': self.secret,
                    'code': authorization_code,
                    'output': 'jsonp'
                }
            )

            if response.ok:
                logging.debug("Succesfully retrieved the refresh and access tokens.")
                response_text = response.text
                access_token = self._extract_access_token(response_text)
                expires_in = self._extract_access_token_expiration(response_text)
                return access_token, expires_in
            else:
                logging.error(
                    "We successfully retrieved the authorization code, but something happened while requesting refresh token and access token")
                raise DeezerClientAuthRefreshAccessTokenException(
                    "We successfully retrieved the authorization code, but something happened while requesting refresh token and access token")

        except requests.exceptions.ConnectionError as e:
            raise MusicSearchProviderConnectionError(
                "Connection error, could not connnect to Deezer Services : {}".format(e.message))

    def _check_credentials_validity(self):
        if not (len(self.app_id) * len(self.secret)):
            raise MusicSearchCredentialsError("Could not find client_id or client_secret")

    def _extract_access_token(self, response):
        values = [param_value.split('=') for param_value in response.split('&')]
        return str(values[0][1])

    def _extract_access_token_expiration(self, response):
        values = [param_value.split('=') for param_value in response.split('&')]
        return int(values[1][1])

    def _set_access_token_expiration_time(self, response):
        expires_in = self._extract_access_token_expiration(response)
        self.access_token_expiration = time.time() + expires_in

    def execute_query(self, query):
        try:
            response = requests.get(
                query.endpoint,
                params={
                    'access_token': self.access_token,
                    'output': 'jsonp'
                })

            if response.ok:
                return response.text
            else:
                raise MusicSearchProviderConnectionError(
                    "There was a problem while making a request to Deezer: '{} with status code {}',"
                    " while hitting the endpoint {}"
                        .format(response.reason, response.status_code, query.endpoint))
        except requests.exceptions.ConnectionError as e:
            raise MusicSearchProviderConnectionError(
                "There was a problem while querying to Deezer API: {}".format(e.message))


class DeezerAPIQueryBuilder(object):
    ENTITY_TYPES = ["artists", "tracks", "playlists"]

    DEEZER_ENDPOINT = "https://api.deezer.com/user/"
    ME_ROUTE = "me"

    def __init__(self):
        self.endpoint = None

    def set_user_data(self):
        self.endpoint = '{}/{}/'.format(self.DEEZER_ENDPOINT, self.ME_ROUTE)

    def set_entity_type(self, entity_type):
        if entity_type not in self.ENTITY_TYPES:
            raise DeezerQueryBuilderException("The entity type : {} is NOT supported".format(entity_type))

        self.endpoint = '{}/{}/'.format(self.endpoint, entity_type)
