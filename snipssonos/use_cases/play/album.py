from snipssonos.shared.use_case import UseCase
from snipssonos.shared.response_object import ResponseSuccess, ResponseFailure
from snipssonos.shared.feedback import FR_TTS_GENERIC_ERROR, FR_TTS_PLAYING_ALBUM_TEMPLATE


class PlayAlbumUseCase(UseCase):

    def __init__(self, device_discovery_service, music_search_service, music_playback_service):
        self.device_discovery_service = device_discovery_service
        self.music_search_service = music_search_service
        self.music_playback_service = music_playback_service

    def process_request(self, request_object):

        device = self.device_discovery_service.get()

        results_albums = list()

        if request_object.playlist_name and request_object.artist_name and request_object.album_name:  # Album, artist, playlist
            results_albums = self.music_search_service.search_album_for_artist_and_for_playlist(
                request_object.album_name,
                request_object.artist_name,
                request_object.playlist_name)

        if request_object.artist_name and request_object.album_name:  # Album, artist
            results_albums = self.music_search_service.search_album_for_artist(request_object.album_name,
                                                                               request_object.artist_name)

        if request_object.playlist_name and request_object.album_name:  # Album, playlist
            results_albums = self.music_search_service.search_album_in_playlist(request_object.album_name,
                                                                                request_object.playlist_name)

        if request_object.album_name:  # Album
            results_albums = self.music_search_service.search_album(request_object.album_name)

        if len(results_albums):
            first_album = results_albums[0]
            self.music_playback_service.clear_queue(device)
            self.music_playback_service.play(device, first_album)
            tts_feedback = FR_TTS_PLAYING_ALBUM_TEMPLATE.format(first_album.name, first_album.artist_name)
            return ResponseSuccess(feedback=tts_feedback)

        return ResponseFailure.build_resource_error(FR_TTS_GENERIC_ERROR)

