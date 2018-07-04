import requests
import logging

from snipssonos.services.node.query_builder import NodeQueryBuilder
from snipssonos.services.music.search_service import MusicSearchService

from snipssonos.exceptions import MusicSearchProviderConnectionError


class DeezerMusicSearchService(MusicSearchService):
    SERVICE_NAME = "deezer"
    DUMMY_LIST = [""]

    def __init__(self):
        self.query_builder = None

    def set_node_query_builder(self, device_name):
        self.query_builder = NodeQueryBuilder(device_name, self.SERVICE_NAME)

    def get_music_service_name(self):
        return self.SERVICE_NAME

    def search_album(self, album_name):
        search_query = self.query_builder\
            .add_album_result_type()\
            .add_album_filter(album_name)\
            .generate_search_query()
        self.execute_query(search_query)
        return self.DUMMY_LIST

    def search_album_for_artist(self, album_name, artist_name):
        search_query = self.query_builder\
            .add_album_result_type()\
            .add_album_filter(album_name)\
            .add_artist_filter(artist_name)\
            .generate_search_query()
        self.execute_query(search_query)
        return self.DUMMY_LIST

    def search_album_in_playlist(self, album_name, playlist_name):
        logging.info("The method search_album_in_playlist is not implemented, rerouting to search_album")
        return self.search_album(album_name)

    def search_album_for_artist_and_for_playlist(self, album_name, artist_name, playlist_name):
        logging.info("The method search_album_for_artist_and_for_playlist is not implemented, rerouting "
                     "to search_album_for_artist")
        return self.search_album_for_artist(album_name, artist_name)

    def search_track(self, track_name):
        search_query = self.query_builder\
            .add_track_result_type()\
            .add_track_filter(track_name)\
            .generate_search_query()
        self.execute_query(search_query)
        return self.DUMMY_LIST

    def search_track_for_artist(self, track_name, artist_name):
        search_query = self.query_builder\
            .add_track_result_type()\
            .add_track_filter(track_name)\
            .add_artist_filter(artist_name)\
            .generate_search_query()
        self.execute_query(search_query)
        return self.DUMMY_LIST

    def search_track_for_album(self, track_name, album_name):
        logging.info("The method search_track_for_album is not implemented, rerouting to search_track")
        self.search_track(track_name)

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
        search_query = self.query_builder\
            .add_track_result_type()\
            .add_artist_filter(artist_name)\
            .generate_search_query()
        self.execute_query(search_query)
        return self.DUMMY_LIST

    def search_artist_for_playlist(self, artist_name, playlist_name):
        logging.info("The method search_artist_for_playlist is not implemented, rerouting "
                     "to search_track_for_artist")
        return self.search_artist(artist_name)

    def search_playlist(self, playlist_name):
        search_query = self.query_builder\
            .add_playlist_result_type()\
            .add_playlist_filter(playlist_name)\
            .generate_search_query()
        self.execute_query(search_query)
        return self.DUMMY_LIST

    def execute_query(self, query):
        try:
            response = requests.get(query)

            if response.ok:
                return response.text
            else:
                raise MusicSearchProviderConnectionError(
                    "There was a problem while making a request to the Node server: '{} with status code {}',"
                    " while hitting the endpoint {}"
                    .format(response.reason, response.status_code, query))
        except requests.exceptions.ConnectionError as e:
            raise MusicSearchProviderConnectionError(
                "There was a problem while querying to Node server api: {}".format(e.message))




