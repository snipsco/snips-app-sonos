from snipssonos.services.service import Service


class MusicSearchService(Service):  # TODO : Make this class Abstract
    PORT = 5005
    HOST = "localhost"
    PROTOCOL = "http://"

    def __init__(self):
        self.PORT = self.CONFIGURATION['global']['music_search_service_port'] if (
            self.CONFIGURATION['global']['music_search_service_port']) else self.PORT

        self.HOST = self.CONFIGURATION['global']['music_search_service_hostname'] if (
            self.CONFIGURATION['global']['music_search_service_hostname']) else self.HOST

    def search_artist(self, artist_name):
        raise NotImplementedError("search_artist() method not implemented for now.")

    def search_artist_for_playlist(self, artist_name, playlist_name):
        raise NotImplementedError("search_artist_in_playlist() method not implemented for now.")

    # Album
    def search_album(self, album_name):
        raise NotImplementedError("search_album() method not implemented for now.")

    def search_album_in_playlist(self, album_name, playlist_name):
        raise NotImplementedError("search_album_in_playlist() method not implemented for now.")

    def search_album_for_artist(self, album_name, artist_name):
        raise NotImplementedError("search_album_for_artist() method not implemented for now.")

    def search_album_for_artist_and_for_playlist(self, album_name, artist_name, playlist_name):
        raise NotImplementedError("search_album_for_artist_and_for_playlist() method not implemented for now.")

    # Song
    def search_track(self, track_name):
        raise NotImplementedError("search_song() method not implemented for now.")

    def search_track_for_playlist(self, track_name, playlist_name):
        raise NotImplementedError("search_song_for_playlist() method not implemented for now.")

    def search_track_for_artist(self, track_name, artist_name):
        raise NotImplementedError("search_song_for_artist() method not implemented for now.")

    def search_track_for_artist_and_for_playlist(self, track_name, artist_name, playlist_name):
        raise NotImplementedError("search_song_for_artist_and_for_playlist() method not implemented for now.")

    def search_track_for_album(self, track_name, album_name):
        raise NotImplementedError("search_song_for_album() method not implemented for now.")

    def search_track_for_album_and_for_playlist(self, track_name, album_name, playlist_name):
        raise NotImplementedError("search_song_for_album_and_for_playlist() method not implemented for now.")

    def search_track_for_album_and_for_artist(self, track_name, album_name, artist_name):
        raise NotImplementedError("search_song_for_album_and_for_artist() method not implemented for now.")

    def search_track_for_album_and_for_artist_and_for_playlist(self, track_name, album_name, artist_name,
                                                               playlist_name):
        raise NotImplementedError(
            "search_song_for_album_and_for_artist_and_for_playlist() method not implemented for now.")

    # Playlist
    def search_playlist(self, playlist_name):
        raise NotImplementedError("search_playlist() method not implemented for now.")
