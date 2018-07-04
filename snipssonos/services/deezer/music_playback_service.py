from snipssonos.services.music.playback_service import MusicPlaybackService


class DeezerNodeMusicPlaybackService(MusicPlaybackService):  # Dumb playback service to comply with current api

    def play(self, device, music_item):
        return True

    def queue(self, device, music_items):
        return True
