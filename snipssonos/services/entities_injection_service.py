import logging
import json

from snipssonos.helpers.mqtt_client import MqttClient
from snipssonos.exceptions import InvalidEntitySlotName
from snipssonos.services.service import Service


class EntitiesInjectionService(Service):
    MQTT_TOPIC_INJECT = 'hermes/asr/inject'

    def __init__(self, hermes_host):
        self.mqtt_client = MqttClient(hermes_host)
        self.mqtt_client.run()

    def publish_entities(self, entity_slot_name, data):
        payload = self.build_payload(entity_slot_name, data)

        injection_topic = self.MQTT_TOPIC_INJECT
        self.mqtt_client.publish(injection_topic, payload)

    def build_payload(self, entity_slot_name, data):
        entities_payload = dict()
        parsed_data = self.parse_data(entity_slot_name, data)
        entities_payload[entity_slot_name] = parsed_data
        logging.info("Injecting data: %s", parsed_data)
        payload = dict()
        payload["operations"] = [
            [
                "addFromVanilla", entities_payload
            ]
        ]
        payload["crossLanguage"] = "en"
        return json.dumps(payload)

    @staticmethod
    def parse_data(entity_slot_name, data):
        try:
            return {
                'snips/artist': [artist.name for artist in data],
                'snips/song': [track.name for track in data],
                'playlistNameFR': [playlist.name for playlist in data]
            }[entity_slot_name]
        except KeyError:
            raise InvalidEntitySlotName("The entity slot name {} has not been defined"
                                        .format(entity_slot_name))
