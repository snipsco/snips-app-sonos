from snipssonos.shared.use_case import UseCase
from snipssonos.shared.response_object import ResponseSuccess, ResponseFailure
from snipssonos.shared.feedback import TTS_GENERIC_ERROR

class PlayPlaylistUseCase(UseCase):

    def __init__(self, device_discovery_service, music_search_service, music_playback_service):
        self.device_discovery_service = device_discovery_service
        self.music_search_service = music_search_service
        self.music_playback_service = music_playback_service

    def process_request(self, request_object):

        device = self.device_discovery_service.get()

        if request_object.playlist_name:
            results_playlists = self.music_search_service.search_playlist(request_object.playlist_name)
            if len(results_playlists):
                first_result = results_playlists[0]
                self.music_playback_service.play(device, first_result)
            else:
                return ResponseFailure.build_resource_error(TTS_GENERIC_ERROR)

        return ResponseSuccess()
