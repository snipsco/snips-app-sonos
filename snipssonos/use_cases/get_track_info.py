from snipssonos.shared.use_case import UseCase
from snipssonos.shared.response_object import ResponseSuccess, ResponseFailure

from snipssonos.shared.feedback import FR_TTS_TRACK_INFO_NO_TRACKS_ERROR, FR_TTS_TRACK_INFO


class GetTrackInfoUseCase(UseCase):

    def __init__(self, device_discovery_service, device_transport_control_service):
        self.device_discovery_service = device_discovery_service
        self.device_transport_control_service = device_transport_control_service

    def process_request(self, request_object):
        device = self.device_discovery_service.get()
        title, artist = self.device_transport_control_service.get_track_info(device)
        if title and artist:
            tts_feedback = FR_TTS_TRACK_INFO.format(title, artist)
            return ResponseSuccess(feedback=tts_feedback)
        return ResponseFailure.build_resource_error(FR_TTS_TRACK_INFO_NO_TRACKS_ERROR)

