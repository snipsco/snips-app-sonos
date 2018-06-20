import paho.mqtt.client as mqtt


class MqttClient:
    def __init__(self, hermes_host):
        self.client = mqtt.Client()
        self.hermes_host = hermes_host

        self.client.on_publish = self.on_publish

    def run(self):
        self.client.connect(self.hermes_host)

    def publish(self, topic, payload):
        self.client.publish(topic, payload, qos=1)

    def on_publish(client, obj, mid):
        print('mid {}'.format(str(mid)))
