# -*-: coding utf-8 -*-
""" Sonos skill for Snips. """

import codecs
import requests


class SpotifyClient():

    def __init__(self, spotify_refresh_token):
        self.client_id = "765e1498b29949c5a36dbcae4eea8330"
        self.client_secret = "72e1fb080f3a49f99b357fd6b8d79cd7"
        self.refresh_token = spotify_refresh_token
        self.get_user_playlists()
        self.get_user_id()

    def refresh_access_token(self):
        _r = requests.post(
            "https://accounts.spotify.com/api/token",
            data={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "refresh_token",
                "refresh_token": self.refresh_token
            })
        if 'access_token' in _r.json():
            self.access_token = _r.json()['access_token']
        else:
            self.access_token = None

    def get_user_id(self):
        _r = requests.get(
            "https://api.spotify.com/v1/me",
            headers={
                "Authorization": "Bearer {}".format(self.access_token),
            })

        if 'id' in _r.json():
            self.user_id = _r.json()['id']
        else:
            self.user_id = None

    def get_user_playlists(self):
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
            print("Unknown playlist {}".format(name))
            return None
        if 'items' in _r.json():
            return _r.json()['items']
        return None

    def dump_favorite(self, mode, n_items, output_name):
        if mode not in ['artists', 'tracks']:
            raise ValueError("mode argument should be 'artists' or 'tracks")
        self.refresh_access_token()
        all_items = set()
        for time_range in ['long_term', 'medium_term', 'short_term']:
            current_items = []
            n_found_items = 0
            while n_found_items <= n_items:
                _r = requests.get(
                    'https://api.spotify.com/v1/me/top/{}'.format(mode),
                    params={
                        'limit': min(50, n_items - n_found_items),
                        # 50 is the maximum
                        'offset': n_found_items,
                        'time_range': time_range
                    },
                    headers={
                        "Authorization": "Bearer {}".format(self.access_token),
                    }
                )
                current_items.extend(
                    [item['name'] for item in _r.json()['items']])
                if len(current_items) == n_found_items:
                    break
                n_found_items = len(current_items)
            all_items.update(current_items)
        with codecs.open(output_name, 'w', 'utf-8') as f:
            f.write(u"\n".join(all_items))

    def dump_playlists(self, output_name):
        with codecs.open(output_name, 'w', 'utf-8') as f:
            f.write(u"\n".join(self.user_playlists.keys()))

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
            return None
