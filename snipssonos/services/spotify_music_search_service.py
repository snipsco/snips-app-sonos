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
        song_search_query = SpotifyAPIQueryBuilder()\
            .add_song_result_type() \
            .add_search_term(song_name)

        raw_response = self.client.execute_query(song_search_query)
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


class SpotifyAPIQueryBuilder(object):
    def __init__(self):
        self.keyword = ""
        self.field_filters = []
        self.result_type = None

    def add_search_term(self, term):
        if len(term):
            self.keyword = term
        return self

    def add_result_type(self, result_type):
        self.result_type = result_type
        return self

    def add_song_result_type(self):
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





    """def get_user_playlists(self):
        # TODO: get all playlists if there are more than 50 by looping
        # and using the offset parameters
        self.refresh_access_token()
        self.user_playlists = {}
        n_found_playlists = 0
        while True:
            _r = requests.get(
                "https://api.spotify.com/v1/me/playlists",
                params={
                    'limit': 50,
                    'offset': n_found_playlists,
                },
                headers={
                    "Authorization": "Bearer {}".format(self.access_token),
                })
            if 'items' in _r.json():
                items = _r.json()['items']
            else:
                items = []
            self.user_playlists.update({
                playlist['name'].lower(): playlist for
                playlist in items})
            if len(self.user_playlists) == n_found_playlists:
                break
            n_found_playlists = len(self.user_playlists)

    def get_tracks_from_playlist(self, name):
        self.refresh_access_token()
        try:
            _r = requests.get(
                self.user_playlists[name]['tracks']['href'],
                params={
                    'limit': 100
                },
                headers={
                    "Authorization": "Bearer {}".format(self.access_token),
                })
        except KeyError:
            print "Unknown playlist {}".format(name)
            return None
        if 'items' in _r.json():
            return _r.json()['items']
        return None

    def get_top_tracks_from_artist(self, artist):
        self.refresh_access_token()
        # First get artist id
        try:
            _r = requests.get(
                'https://api.spotify.com/v1/search',
                params={
                    'q': artist,
                    'type': 'artist'
                },
                headers={
                    "Authorization": "Bearer {}".format(self.access_token)
                }
            )
            _id = _r.json()['artists']['items'][0]['id']
            # Get list of top tracks from artist
            _r = requests.get(
                'https://api.spotify.com/v1/artists/{}/top-tracks'.format(_id),
                params={
                    'country': 'fr'
                },
                headers={
                    "Authorization": "Bearer {}".format(self.access_token)
                }
            )
            return _r.json()['tracks']
        except Exception:
            return None

    def get_track(self, song):
        self.refresh_access_token()
        try:
            _r = requests.get(
                'https://api.spotify.com/v1/search',
                params={
                    'q': song,
                    'type': 'track'
                },
                headers={
                    "Authorization": "Bearer {}".format(self.access_token)
                }
            )
            # return best match
            return _r.json()['tracks']['items'][0]
        except Exception:
            return None

    def get_tracks_from_album(self, album):
        self.refresh_access_token()
        try:
            _r = requests.get(
                'https://api.spotify.com/v1/search',
                params={
                    'q': album,
                    'type': 'album'
                },
                headers={
                    "Authorization": "Bearer {}".format(self.access_token)
                }
            )
            # return best match
            album = _r.json()['albums']['items'][0]
            _r = requests.get(
                'https://api.spotify.com/v1/albums/{}/tracks'.format(album['id']),
                params={},
                headers={
                    "Authorization": "Bearer {}".format(self.access_token)
                }
            )
            return _r.json()['items']
        except Exception:
            return None

    def add_song(self, artist, song):
        self.refresh_access_token()
        # First, get the id of the song
        track = self.get_track("track:" + '"' + song + '"' + ' artist:' + '"' + artist + '"')
        try:
            requests.put(
                'https://api.spotify.com/v1/me/tracks',
                params={
                    "ids": track['id']
                },
                headers={
                    "Authorization": "Bearer {}".format(self.access_token)
                }
            )
        except Exception:
            return None"""