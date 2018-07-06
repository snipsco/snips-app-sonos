import logging

from snipssonos.shared.use_case import UseCase
from snipssonos.shared.response_object import ResponseSuccess, ResponseFailure


class InjectEntitiesUseCase(UseCase):

    def __init__(self, music_customization_service, entities_injection_service):
        self.music_customization_service = music_customization_service
        self.entities_injection_service = entities_injection_service

    def process_request(self, request_object):
        self.entities_injection_service.publish_entities(self.music_customization_service,
                                                         request_object.entities_type)
        return ResponseSuccess()

