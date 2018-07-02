import logging

from snipssonos.shared.use_case import UseCase
from snipssonos.shared.response_object import ResponseSuccess, ResponseFailure


class InjectEntitiesUseCase(UseCase):

    def __init__(self, music_customization_service, entities_injection_service):
        self.music_customization_service = music_customization_service
        self.entities_injection_service = entities_injection_service

    def process_request(self, request_object):
        entities = request_object.entities

        for entity_name, entity_slot_name in entities.iteritems():
            logging.info("Inject entities request made for '{}' with slot name '{}'"
                         .format(entity_name, entity_slot_name))
            results_entity = self.music_customization_service.fetch_entity(entity_name)
            if len(results_entity):
                self.entities_injection_service.build_entities_payload(entity_slot_name, results_entity)
            else:
                return ResponseFailure.build_resource_error("An error occurred, service return an empty response")
        self.entities_injection_service.publish_entities()
        return ResponseSuccess()
