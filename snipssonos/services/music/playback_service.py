from snipssonos.services.service import ConfigurableHTTPService


class MusicPlaybackService(ConfigurableHTTPService):

    def __init__(self, device=None, CONFIGURATION=None):
        super(MusicPlaybackService, self).__init__(CONFIGURATION)
        self.device = device

    def play(self, device, artist_name):
        raise NotImplementedError("play() method not implemented for now.")

    def queue(self, device, music_items):
        raise NotImplementedError("queue() method not implemented for now.")
