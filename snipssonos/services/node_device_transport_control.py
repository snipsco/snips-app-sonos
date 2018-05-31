import requests

from snipssonos.services.device_transport_control import DeviceTransportControlService
from snipssonos.exceptions import NoReachableDeviceException

class NodeDeviceTransportControlService(DeviceTransportControlService):

    PORT = 5005
    HOST = "localhost"
    PROTOCOL = "http://"

    BASE_URL = "{}{}:{}".format(PROTOCOL, HOST, PORT)

    def pause(self, device):
        room_name = device.name
        query_url = self._generate_pause_query(room_name)
        return self._process_query(query_url)

    def resume(self, device):
        room_name = device.name
        query_url = self._generate_resume_query(room_name)

        return self._process_query(query_url)

    def _generate_pause_query(self, room_name):
        return "{}/{}/pause".format(self.BASE_URL, room_name)

    def _generate_resume_query(self, room_name):
        return "{}/{}/play".format(self.BASE_URL, room_name)

    def _generate_volume_query(self, room_name, volume_level):
        return "{}/{}/volume/{}".format(self.BASE_URL, room_name, volume_level)

    def _process_query(self, query_url):
        req = requests.get(query_url)
        if req.ok:
            return True
        raise NoReachableDeviceException("Could not reach your Sonos device")

    def volume_up(self, device):
        return self.set_volume(device)

    def volume_down(self, device):
        return self.set_volume(device)

    def set_volume(self, device):
        room_name = device.name
        volume_level = device.volume

        query_url = self._generate_volume_query(room_name, volume_level)

        return self._process_query(query_url)

