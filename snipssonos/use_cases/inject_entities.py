import logging
from snipssonos.shared.use_case import UseCase
from snipssonos.shared.response_object import ResponseSuccess, ResponseFailure


class InjectEntitiesUseCase(UseCase):

    def __init__(self, music_customization_service, entities_injection_service):
        self.music_customization_service = music_customization_service
        self.entities_injection_service = entities_injection_service

    def process_request(self, request_object):
        entity_name = request_object.entity_name
        results_entity = self.music_customization_service.fetch_entity(entity_name)
        if len(results_entity):
            self.entities_injection_service.publish_entities(request_object.entity_slot_name, results_entity)
        else:
            return ResponseFailure.build_resource_error("An error occurred, service return an empty response")

        return ResponseSuccess()
