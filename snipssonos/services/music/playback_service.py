from snipssonos.services.service import Service


class MusicPlaybackService(Service):
    PORT = 5005
    HOST = "localhost"
    PROTOCOL = "http://"

    def __init__(self, device=None):
        self.device = device

        self.PORT = self.CONFIGURATION['global']['music_playback_service_port'] if (
            self.CONFIGURATION['global']['music_service_port']) else self.PORT

        self.HOST = self.CONFIGURATION['global']['music_service_hostname'] if (
            self.CONFIGURATION['global']['music_service_hostname']) else self.HOST

    def play(self, device, artist_name):
        raise NotImplementedError("play() method not implemented for now.")

    def queue(self, device, music_items):
        raise NotImplementedError("queue() method not implemented for now.")
