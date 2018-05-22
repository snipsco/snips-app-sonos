# TODO : Make this abstract
class SpeakerControllerAction(object):
    """
    an interface to interact with intents following the ontology of the "Music Player" assistant.
    """
    def __init__(self):
        pass

    def volume_down(self, volume_request):
        pass

    def volume_up(self, volume_request):
        pass

    def previous_song(self, request):
        pass

    def next_song(self, request):
        pass

    def speaker_interrupt(self, request):
        pass

    def resume_music(self, request):
        pass

    def play_song(self, song_request):
        pass

    def play_artist(self, artist_request):
        pass

    def play_album(self, album_request):
        pass

    def play_playlist(self, playlist_request):
        pass

    def get_infos(self, info_request):
        pass

    def add_song(self, request):
        pass

    def radio_on(self, radio_on_request):
        pass
