import requests

from snipssonos.services.device_transport_control import DeviceTransportControlService
from snipssonos.exceptions import NoReachableDeviceException

class NodeDeviceTransportControlService(DeviceTransportControlService):

    PORT = 5005
    HOST = "localhost"
    PROTOCOL = "http://"

    def volume_up(self, device):
        room_name = device.name
        volume_level = device.volume

        query_url = self.generate_volume_up_query(room_name, volume_level)

        req = requests.get(query_url)
        if req.ok:
            return True
        raise NoReachableDeviceException("Could not reach your Sonos device")

    def generate_volume_up_query(self, room_name, volume_increment):
        return "{}{}:{}/{}/volume/{}".format(self.PROTOCOL, self.HOST, self.PORT, room_name, volume_increment)

