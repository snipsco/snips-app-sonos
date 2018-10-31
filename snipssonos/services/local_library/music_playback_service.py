from snipssonos.services.deezer.music_playback_service import DeezerNodeMusicPlaybackService


class LocalLibraryNodeMusicPlaybackService(DeezerNodeMusicPlaybackService):
    """
    The playback service for Deezer behaves dumbly to comply with current API on how the play
    requests are processed.
    We are currently using a service that call to a middleware (Node Sonos server) that handles the
    search and then it drectly plays the results of the search.
    """
    pass
