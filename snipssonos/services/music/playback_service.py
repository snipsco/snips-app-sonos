class MusicPlaybackService(object):

    def __init__(self, device=None):
        self.device = device

    def play(self, device, artist_name):
        raise NotImplementedError("play() method not implemented for now.")

    def queue(self, device, music_items):
        raise NotImplementedError("queue() method not implemented for now.")

    def clear_queue(self, device):
        raise NotImplementedError("clear_queue() method not implemented for now.")
