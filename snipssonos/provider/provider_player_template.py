from abc import ABCMeta

class ProviderPlayerTemplate():
    __metaclass__ = ABCMeta
    def __init__(self):
        raise NotImplementedError("Please implement the __init__ method")

    def play_artist(self, device, name, shuffle=False):
        return False

    def play_track(self, device, name, shuffle=False):
        return False

    def play_album(self, device, name, shuffle=False):
        return False

    def play_playlist(self, device, name, shuffle=False):
        return False

    def play_station(self, device, name, shuffle=False):
        return False

    def play_genre(self, device, name, shuffle=False):
        return False

    def play_tag(self, device, name, shuffle=False):
        return False
