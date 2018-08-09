import base64
import logging
import requests
import time

from snipssonos.exceptions import MusicSearchProviderConnectionError, MusicSearchCredentialsError, \
    DeezerClientAuthorizationException, DeezerClientAuthRefreshAccessTokenException


class DeezerClient(object):
    """
    This class contains helper methods to request the Deezer Web API.
    It covers all endpoints of the API, but most helpers functions are for authentication.

    Please refer to the Authorization Code Flow section on this page : https://developers.deezer.com/api/oauth
    """
    AUTH_SERVICE_ENDPOINT = "https://connect.deezer.com/oauth/access_token.php"

    def __init__(self, app_id, secret):
        self.app_id = str(app_id)
        self.secret = str(secret)
        self.access_token = None
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

                access_token = self._extract_access_token(response)
                expires_in = self._extract_access_token_expiration(response)
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
        values = [param_value.split('=') for param_value in response.text.split('&')]
        return str(values[0][1])

    def _extract_access_token_expiration(self, response):
        values = [param_value.split('=') for param_value in response.text.split('&')]
        return int(values[1][1])

    def _set_access_token_expiration_time(self, response):
        expires_in = self._extract_access_token_expiration(response)
        self.access_token_expiration = time.time() + expires_in

    def authenticate(self):
        """
        This method is used to refresh the access token.
        """
        if self.access_token is None or time.time() > self.access_token_expiration:
            self.access_token = self.retrieve_access_token()

    def execute_query(self, query):
        try:
            self.authenticate()
            response = requests.get(
                query.endpoint,
                params=query.params_to_dict())

            if response.ok:
                return response.text
            else:
                raise MusicSearchProviderConnectionError(
                    "There was a problem while making a request to Deezer: '{} with status code {}',"
                    " while hitting the endpoint {}"
                        .format(response.reason, response.status_code, query.endpoint))
        except requests.exceptions.ConnectionError as e:
            raise MusicSearchProviderConnectionError(
                "There was a problem while querying to Deezer api: {}".format(e.message))

