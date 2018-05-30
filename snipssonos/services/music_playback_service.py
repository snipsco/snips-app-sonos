class MusicPlaybackService(object):

    def __init__(self, device):
        self.device = device

    def play(self, artist_name):
        raise NotImplementedError("play() method not implemented for now.")
