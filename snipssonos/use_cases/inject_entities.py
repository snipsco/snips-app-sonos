import logging
from snipssonos.shared.use_case import UseCase
from snipssonos.shared.response_object import ResponseSuccess, ResponseFailure


class InjectEntitiesUseCase(UseCase):

    def __init__(self, music_customization_service, entities_injection_service):
        self.music_customization_service = music_customization_service
        self.entities_injection_service = entities_injection_service

    def process_request(self, request_object):
        if request_object.entity_name:
            logging.info("Fetching top artists")
            results_artist = self.music_customization_service.fetch_top_artist()
            self.music_customization_service.reset_user_endpoint()
            if len(results_artist):
                logging.info("Injecting artists: {}".format(results_artist))
                self.entities_injection_service.publish_entities(request_object.entity_name, results_artist)
            else:
                return ResponseFailure.build_resource_error("An error occurred")

        return ResponseSuccess()
