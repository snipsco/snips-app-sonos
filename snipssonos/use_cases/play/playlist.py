from snipssonos.shared.use_case import UseCase
from snipssonos.shared.response_object import ResponseSuccess, ResponseFailure


class PlayPlaylistUseCase(UseCase):

    def __init__(self, device_discovery_service, music_search_service, music_playback_service, feedback_service):
        self.device_discovery_service = device_discovery_service
        self.music_search_service = music_search_service
        self.music_playback_service = music_playback_service
        self.feedback_service = feedback_service

    def process_request(self, request_object):

        device = self.device_discovery_service.get()
        results_playlists = list()

        if request_object.playlist_name:
            results_playlists = self.music_search_service.search_playlist(request_object.playlist_name)

        if len(results_playlists):
            first_playlist = results_playlists[0]
            self.music_playback_service.clear_queue(device)
            self.music_playback_service.play(device, first_playlist)
            tts_feedback = self.feedback_service.get_playlist_template()\
                .format(first_playlist.name)
            return ResponseSuccess(feedback=tts_feedback)

        return ResponseFailure.build_resource_error(self.feedback_service.get_generic_error_message())
