from snipssonos.shared.use_case import UseCase
from snipssonos.shared.response_object import ResponseSuccess, ResponseFailure


class InjectEntitiesUseCase(UseCase):

    def __init__(self, music_custom_service, inject_entities_service):
        self.music_custom_service = music_custom_service
        self.inject_entities_service = inject_entities_service

    def process_request(self, request_object):
        if request_object.entity_name:
            results_artist = self.music_custom_service.fetch_top_artist()
            self.music_custom_service.reset_user_endpoint()
            if len(results_artist):
                self.inject_entities_service.publish_entities(request_object.entity_name, results_artist)
            else:
                return ResponseFailure.build_resource_error("An error occurred")

        return ResponseSuccess()
