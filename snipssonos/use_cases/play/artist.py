from snipssonos.shared.use_case import UseCase
from snipssonos.shared.response_object import ResponseSuccess, ResponseFailure

from snipssonos.shared.feedback import FR_TTS_GENERIC_ERROR  # TODO : This might violate the dependency rule of clean Architecture ...


class PlayArtistUseCase(UseCase):

    def __init__(self, device_discovery_service, music_search_service, music_playback_service):
        self.device_discovery_service = device_discovery_service
        self.music_search_service = music_search_service
        self.music_playback_service = music_playback_service

    def process_request(self, request_object):

        device = self.device_discovery_service.get()

        results_track = list()

        if request_object.playlist_name and request_object.artist_name:
            results_track = self.music_search_service.search_artist_for_playlist(request_object.artist_name,
                                                                                 request_object.playlist_name)

        if request_object.artist_name:
            results_track = self.music_search_service.search_artist(request_object.artist_name)

        if len(results_track) > 1:
            first_result = results_track[0]
            other_results = results_track[1:]

            self.music_playback_service.clear_queue(device)
            self.music_playback_service.play(device, first_result)
            self.music_playback_service.queue(device, other_results)

        elif len(results_track) == 1:
            first_result = results_track[0]
            self.music_playback_service.clear_queue(device)
            self.music_playback_service.play(device, first_result)
        else:
            return ResponseFailure.build_resource_error(FR_TTS_GENERIC_ERROR)

        return ResponseSuccess()
