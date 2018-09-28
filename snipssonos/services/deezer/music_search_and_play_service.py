from __future__ import unicode_literals

import requests
import logging

from requests import ConnectionError

from snipssonos.entities.album import Album
from snipssonos.entities.artist import Artist
from snipssonos.entities.playlist import Playlist
from snipssonos.entities.track import Track
from snipssonos.services.node.query_builder import DeezerNodeQueryBuilder
from snipssonos.services.music.search_service import MusicSearchService
from snipssonos.services.music.playback_service import MusicPlaybackService

from snipssonos.exceptions import MusicSearchProviderConnectionError


class DeezerMusicSearchService(MusicSearchService, MusicPlaybackService):
    """
    This service is able to search and directly play music on the Sonos device. The middleware we are
    using to search and play is the Node Sonos server and  it does not offer a way to play songs coming from
    Deezer through an ID. What it does offer is an endpoint to be able to do the search and then play
    the results directly.
    """
    SERVICE_NAME = "deezer"
    DUMMY_LIST = [""]

    def __init__(self, device_discovery_service):
        self.device_discovery_service = device_discovery_service
        first_device = self.device_discovery_service.get()
        self.query_builder = DeezerNodeQueryBuilder(first_device.name)

    def search_album(self, album_name):
        search_query = self.query_builder \
            .reset_field_filters() \
            .add_album_result_type() \
            .add_album_filter(album_name) \
            .generate_search_query()
        self.execute_query(search_query)
        return [Album("", album_name)]

    def search_album_for_artist(self, album_name, artist_name):
        search_query = self.query_builder \
            .reset_field_filters() \
            .add_album_result_type() \
            .add_album_filter(album_name) \
            .add_artist_filter(artist_name) \
            .generate_search_query()

        self.execute_query(search_query)
        return [Album("", album_name, [Artist("", artist_name)])]

    def search_album_in_playlist(self, album_name, playlist_name):
        logging.info("The method search_album_in_playlist is not implemented, rerouting to search_album")
        return self.search_album(album_name)

    def search_album_for_artist_and_for_playlist(self, album_name, artist_name, playlist_name):
        logging.info("The method search_album_for_artist_and_for_playlist is not implemented, rerouting "
                     "to search_album_for_artist")
        return self.search_album_for_artist(album_name, artist_name)

    def search_track(self, track_name):
        search_query = self.query_builder \
            .reset_field_filters() \
            .add_track_result_type() \
            .add_track_filter(track_name) \
            .generate_search_query()
        self.execute_query(search_query)
        return [Track("", track_name)]

    def search_track_for_artist(self, track_name, artist_name):
        search_query = self.query_builder \
            .reset_field_filters() \
            .add_track_result_type() \
            .add_track_filter(track_name) \
            .add_artist_filter(artist_name) \
            .generate_search_query()
        self.execute_query(search_query)
        return [Track("", track_name, [Artist("", artist_name)])]

    def search_track_for_album(self, track_name, album_name):
        logging.info("The method search_track_for_album is not implemented, rerouting to search_track")
        search_query = self.query_builder \
            .reset_field_filters() \
            .add_track_result_type() \
            .add_track_filter(track_name) \
            .add_album_filter(album_name) \
            .generate_search_query()

        self.execute_query(search_query)
        return [Track("", track_name)]

    def search_track_for_playlist(self, track_name, playlist_name):
        logging.info("The method search_track_for_playlist is not implemented, rerouting to search_track")
        return self.search_track(track_name)

    def search_track_for_album_and_for_artist(self, track_name, album_name, artist_name):
        logging.info("The method search_track_for_album_and_for_artist is not implemented, rerouting "
                     "to search_track_for_artist")
        return self.search_track_for_artist(track_name, artist_name)

    def search_track_for_album_and_for_playlist(self, track_name, album_name, playlist_name):
        logging.info("The method search_track_for_album_and_for_playlist is not implemented, rerouting to search_track")
        return self.search_track(track_name)

    def search_track_for_artist_and_for_playlist(self, track_name, artist_name, playlist_name):
        logging.info("The method search_track_for_artist_and_for_playlist is not implemented, rerouting "
                     "to search_track_for_artist")
        return self.search_track_for_artist(track_name, artist_name)

    def search_track_for_album_and_for_artist_and_for_playlist(self, track_name, album_name, artist_name,
                                                               playlist_name):
        logging.info("The method search_track_for_album_and_for_artist_and_for_playlist is not implemented, rerouting "
                     "to search_track_for_artist")
        return self.search_track_for_artist(track_name, artist_name)

    def search_artist(self, artist_name):
        search_query = self.query_builder \
            .reset_field_filters() \
            .add_track_result_type() \
            .add_artist_filter(artist_name) \
            .generate_search_query()
        self.execute_query(search_query)
        return [Artist("", artist_name)]

    def search_artist_for_playlist(self, artist_name, playlist_name):
        logging.info("The method search_artist_for_playlist is not implemented, rerouting "
                     "to search_track_for_artist")
        return self.search_artist(artist_name)

    def search_playlist(self, playlist_name):
        search_query = self.query_builder \
            .reset_field_filters() \
            .add_playlist_result_type() \
            .add_playlist_filter(playlist_name) \
            .generate_search_query()
        self.execute_query(search_query)
        return [Playlist("", playlist_name)]

    def execute_query(self, query):
        try:
            response = requests.get(query)
            if not response.ok:
                raise MusicSearchProviderConnectionError(
                    "There was a problem while making a request to the Node server: '{} with status code {}',"
                    " while hitting the endpoint {}"
                        .format(response.reason, response.status_code, query))
        except ConnectionError as e:
            raise MusicSearchProviderConnectionError(
                "There was a problem while querying to Node server api: {}".format(e.message))
