from __future__ import unicode_literals

from snipssonos.exceptions import NodeQueryBuilderMissingQueryData, NodeQueryBuilderUnavailableMusicService


class NodeQueryBuilder(object):
    AVAILABLE_MUSIC_SERVICES = ["spotify", "deezer"]

    PORT = 5005
    HOST = "localhost"
    PROTOCOL = "http://"

    def __init__(self, device_name, music_service):
        self.device_name = device_name
        self.music_service = music_service
        self.result_type = None
        self.field_filters = []

    def set_music_service(self, music_service):
        if self.is_available_music_service(music_service):
            self.music_service = music_service
        else:
            raise NodeQueryBuilderUnavailableMusicService(
                "The {} is not available {} use instead"
                    .format(music_service, ','.join(self.AVAILABLE_MUSIC_SERVICES)))

    def reset_field_filters(self):
        self.field_filters = list()
        return self

    def add_field_filter(self, music_field_key, music_field_value):
        if (music_field_value is None) or len(music_field_value) == 0:
            raise NodeQueryBuilderMissingQueryData("Music field : {} has an empty value. The query is not valid. ".format(music_field_key))

        self.field_filters.append((music_field_key, music_field_value))
        return self

    def add_result_type(self, result_type):
        self.result_type = result_type
        return self

    def add_track_result_type(self):
        return self.add_result_type("song")

    def add_album_result_type(self):
        return self.add_result_type("album")

    def add_playlist_result_type(self):
        return self.add_result_type("playlist")

    def add_track_filter(self, track_name):
        self.add_field_filter("track", track_name)
        return self

    def add_artist_filter(self, artist_name):
        self.add_field_filter("artist", artist_name)
        return self

    def add_album_filter(self, album_name):
        self.add_field_filter("album", album_name)
        return self

    def add_playlist_filter(self, playlist_name):
        self.add_field_filter("playlist", playlist_name)
        return self

    def _generate_base_endpoint(self):
        return "{}{}:{}".format(self.PROTOCOL, self.HOST, self.PORT)

    def _generate_query_terms(self):
        if len(self.field_filters) == 0:
            return ''

        if len(self.field_filters) == 1:  # There's a single search term.
            return ''.join([filter_value for (filter_type, filter_value) in self.field_filters])

        return ':'.join(
            map(lambda field_filter: '{}:"{}"'.format(field_filter[0], field_filter[1]), self.field_filters))

    def generate_search_query(self):
        device_name = self.device_name
        base_endpoint = self._generate_base_endpoint()
        fields_query = self._generate_query_terms()
        if self.result_type and fields_query:
            return "{}/{}/musicsearch/{}/{}/{}".format(base_endpoint, device_name, self.music_service,
                                                       self.result_type, fields_query)
        else:
            raise NodeQueryBuilderMissingQueryData("Result type and/or field filters have not been set")

    def is_available_music_service(self, music_service):
        return music_service in self.AVAILABLE_MUSIC_SERVICES


class DeezerNodeQueryBuilder(NodeQueryBuilder):
    def __init__(self, device_name):
        super(DeezerNodeQueryBuilder, self).__init__(device_name, "deezer")


class SpotifyNodeQueryBuilder():
    def __init__(self, device_name):
        super(DeezerNodeQueryBuilder, self).__init__(device_name, "spotify")
