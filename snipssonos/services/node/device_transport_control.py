import requests

from snipssonos.services.device.transport_control import DeviceTransportControlService
from snipssonos.exceptions import NoReachableDeviceException


class NodeDeviceTransportControlService(DeviceTransportControlService):
    BASE_URL = "{}{}:{}".format(DeviceTransportControlService.PROTOCOL, DeviceTransportControlService.HOST,
                                DeviceTransportControlService.PORT)

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

    def _generate_mute_query(self, room_name):
        return "{}/{}/mute".format(self.BASE_URL, room_name)

    def _generate_next_track_query(self, room_name):
        return "{}/{}/next".format(self.BASE_URL, room_name)

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

    def mute(self, device):
        room_name = device.name
        query_url = self._generate_mute_query(room_name)
        return self._process_query(query_url)

    def next_track(self, device):
        room_name = device.name
        query_url = self._generate_next_track_query(room_name)
        return self._process_query(query_url)
