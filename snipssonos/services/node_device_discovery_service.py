import json
import requests

from snipssonos.entities.device import Device
from snipssonos.services.device_discovery_service import DeviceDiscoveryService
from snipssonos.exceptions import DeviceParsingException, NoReachableDeviceException


class NodeDeviceDiscoveryService(DeviceDiscoveryService):
    PORT = 5005
    HOST = "localhost"
    PROTOCOL = "http://"

    def get(self):
        devices = self.get_devices()
        if len(devices):
            return devices[0]
        else:
            raise NoReachableDeviceException("Couldn't find any reachable device")

    def get_devices(self):
        response = self.execute_query()
        return self.parse_devices(response)

    def execute_query(self):
        query_url = self.generate_get_query()

        req = requests.get(query_url)

        if req.ok:
            return req.text
        raise NoReachableDeviceException("Could not reach your Sonos devices")

    def generate_get_query(self):
        return "{}{}:{}/zones/".format(self.PROTOCOL, self.HOST, self.PORT)

    def parse_devices(self, json_response):
        parsed_response = json.loads(json_response)

        try:
            members_section = parsed_response[0]['members']
            devices = [Device(member['uuid'], member['roomName'], member['state']['volume']) for member in members_section]
        except KeyError as e:
            raise DeviceParsingException(e.message)

        return devices
