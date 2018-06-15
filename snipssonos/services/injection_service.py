import json

from snipssonos.helpers.mqtt_client import MqttClient


class InjectEntitiesService:
    MQTT_TOPIC_INJECT = 'hermes/asr/inject'

    def __init__(self, hermes_host):
        self.mqtt_client = MqttClient(hermes_host)
        self.mqtt_client.run()

        self.data = None
        self.entity_name = None

    def publish_entities(self, entity_name, data):
        self.data = data
        self.entity_name = entity_name
        payload = self.build_payload()

        print(payload)

        injection_topic = self.MQTT_TOPIC_INJECT
        self.mqtt_client.publish(injection_topic, payload)

    def build_payload(self):
        entities_payload = dict()
        entities_payload[self.entity_name] = self.parse_data()

        payload = dict()
        payload["operations"] = [
                [
                    "addFromVanilla", entities_payload
                ]
            ]
        payload["crossLanguage"] = "en"

        return json.dumps(payload)

    def parse_data(self):
        return {
            'artistNameFR': [artist.name for artist in self.data],
            'song_name': {},
            'playlist_name': {}
        }[self.entity_name]


# TODO erase, just for test
if __name__ == "__main__":
    from snipssonos.use_cases.request_objects import InjectEntitiesRequestObject
    from snipssonos.entities.artist import Artist

    HOSTNAME = "localhost"

    inject = InjectEntitiesService(HOSTNAME)
    inject_entities_request = InjectEntitiesRequestObject("artistNameFR")

    artists = [Artist(None, 'pau fabregat'), Artist(None, 'blabla')]

    inject.publish_entities(inject_entities_request.entity_name, artists)
