from .provider_player_template import A_ProviderPlayerTemplate
import soco

class LocalPlayer(A_ProviderPlayerTemplate):

    def __init__(self, device):
        try:
            self.my_library = soco.music_library.MusicLibrary(device)
        except Exception:
            self.my_library = None

    def play(self, device, name, shuffle=False, func=None):
        if self.my_library is None:
            return False
        tracks = func(search_term = name)
        if not tracks or tracks[0] is None:
            return False
        track = tracks[0]
        device.stop()
        device.clear_queue()
        device.add_to_queue(track)
        if shuffle:
            device.play_mode("SHUFFLE_NOREPEAT")
        device.play_from_queue(0)
        return True

    def play_track(self, device, name, shuffle=False):
        return self.play(device, name, shuffle, self.my_library.get_tracks) or\
                self.play(device, name, shuffle, device.music_library.get_tracks)

    def play_artist(self, device, name, shuffle=False):
        return self.play(device, name, shuffle, self.my_library.get_artists) or\
                self.play(device, name, shuffle, device.music_library.get_artists)


    def play_album(self, device, name, shuffle=False):
        return self.play(device, name, shuffle, self.my_library.get_albums) or\
                self.play(device, name, shuffle, device.music_library.get_albums)

    def play_playlist(self, device, name, shuffle=False):
        return self.play(device, name, shuffle, self.my_library.get_playlists)\
                or self.play_sonos_playlist(device, name, shuffle)

    def play_sonos_playlist(self, device, name, shuffle=False):
        playlists =list(device.get_sonos_playlists())
        if not playlists:
            return False
        for playlist in playlists:
            if (playlist.title == name):
                device.stop()
                device.clear_queue()
                device.add_to_queue(playlist)
                if shuffle:
                    device.play_mode("SHUFFLE_NOREPEAT")
                device.play_from_queue(0)
                return True
        return False
