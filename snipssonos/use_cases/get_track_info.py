from snipssonos.shared.use_case import UseCase
from snipssonos.shared.response_object import ResponseSuccess, ResponseFailure


class GetTrackInfoUseCase(UseCase):

    def __init__(self, device_discovery_service, device_transport_control_service, feedback_service):
        self.device_discovery_service = device_discovery_service
        self.device_transport_control_service = device_transport_control_service
        self.feedback_service = feedback_service

    def process_request(self, request_object):
        device = self.device_discovery_service.get()
        track, artist = self.device_transport_control_service.get_track_info(device)
        title = track.name
        artist_name = artist.name
        if title and artist_name:
            tts_feedback = self.feedback_service.get_track_info_template()\
                .format(title, artist_name)
            return ResponseSuccess(feedback=tts_feedback)
        return ResponseFailure.build_resource_error(self.feedback_service.get_no_tracks_error_message())

