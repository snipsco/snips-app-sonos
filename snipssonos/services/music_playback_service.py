class MusicPlaybackService(object):

    def __init__(self, device=None):
        self.device = device


    def play(self, device, artist_name):
        raise NotImplementedError("play() method not implemented for now.")
