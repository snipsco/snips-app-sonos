from snipssonos.services.music.playback_service import MusicPlaybackService


class DeezerNodeMusicPlaybackService(MusicPlaybackService):
    """
    The playback service for Deezer behaves dumbly to comply with current API on how the play
    requests are processed.
    We are currently using a service that call to a middleware (Node Sonos server) that handles the
    search and then it drectly plays the results of the search.
    """

    def play(self, device, music_item):
        return True

    def queue(self, device, music_items):
        return True

    def clear_queue(self, device):
        return True
