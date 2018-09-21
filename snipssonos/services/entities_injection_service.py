import logging
import json

from snipssonos.helpers.mqtt_client import MqttClient
from snipssonos.exceptions import InvalidEntitySlotName
from snipssonos.services.service import Service


class EntitiesInjectionService(Service):
    MQTT_TOPIC_INJECT = 'hermes/injection/perform'

    def __init__(self, hermes_host):
        self.mqtt_client = MqttClient(hermes_host)
        self.mqtt_client.run()

        self.entities_payload = dict()

    def publish_entities(self, music_customization_service, entities_type):
        for entity_name, entity_slot_name in entities_type.iteritems():
            logging.info("Inject entities request made for '{}' with slot name '{}'"
                         .format(entity_name, entity_slot_name))
            results_entity = music_customization_service.fetch_entity(entity_name)
            if len(results_entity):
                self.build_entities_payload(entity_slot_name, results_entity)
        payload = self.build_payload()

        injection_topic = self.MQTT_TOPIC_INJECT
        self.mqtt_client.publish(injection_topic, payload)
        self.entities_payload = dict()

    def build_entities_payload(self, entity_slot_name, data):
        parsed_data = self.parse_data(entity_slot_name, data)
        self.entities_payload[entity_slot_name] = parsed_data
        logging.info("Data to be injected: %s", parsed_data)

    def build_payload(self):
        payload = dict()
        payload["operations"] = [
                [
                    "addFromVanilla", self.entities_payload
                ]
            ]
        payload["crossLanguage"] = "en"
        return json.dumps(payload)

    @staticmethod
    def parse_data(entity_slot_name, data):
        try:
            return {
                'snips/musicArtist': [artist.name for artist in data],
                'snips/musicTrack': [track.name for track in data],
                'playlistNameFR': [playlist.name for playlist in data]
            }[entity_slot_name]
        except KeyError:
            raise InvalidEntitySlotName("The entity slot name {} has not been defined"
                                        .format(entity_slot_name))
