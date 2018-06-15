import paho.mqtt.client as mqtt
import time

class MqttClient:
    MQTT_TOPIC_INJECT_MUSIC = 'hermes/asr/inject'

    def __init__(self, hermes_host):
        self.client = mqtt.Client()
        self.hermes_host = hermes_host

        self.client.on_publish = self.on_publish
        # self.client.on_connect = self.on_connect
        # self.client.on_message = self.on_message

    def run(self):
        self.client.connect(self.hermes_host)
        # self.client.loop_forever()

    def publish(self, topic, payload):
        self.client.publish(topic, payload, qos=1)
        # self.client.loop_forever()

    def on_publish(client, obj, mid):
        print('mid {}'.format(str(mid)))

    # def on_connect(self, client, userdata, flags, rc):
    #     print("Connected with result code " + str(rc))
    #
    #     # Subscribing in on_connect() means that if we lose the connection and
    #     # reconnect then subscriptions will be renewed.
    #     client.subscribe("$SYS/#")
    #     info = self.client.publish('hermes/asr/inject', "bla", qos=1)
    #     print(info.is_published())
    #
    # def on_message(self, client, userdata, msg):
    #     print(msg.topic + " " + str(msg.payload))
