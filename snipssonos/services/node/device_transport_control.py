import requests

from snipssonos.services.device.transport_control import DeviceTransportControlService
from snipssonos.entities.track import Track
from snipssonos.entities.artist import Artist
from snipssonos.exceptions import NoReachableDeviceException


class NodeDeviceTransportControlService(DeviceTransportControlService):
    SERVICE_NAME = "node_device_transport_control"

    def __init__(self, configuration=None):
        super(NodeDeviceTransportControlService, self).__init__(configuration)
        self.BASE_URL = "{}{}:{}".format(self.PROTOCOL, self.HOST,
                                         self.PORT)

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

    def _generate_previous_track_query(self, room_name):
        return "{}/{}/previous".format(self.BASE_URL, room_name)

    def _generate_state_query(self, room_name):
        return "{}/{}/state".format(self.BASE_URL, room_name)

    def _generate_track_seek_query(self, room_name, track_number):
        return "{}/{}/trackseek/{}".format(self.BASE_URL, room_name, track_number)

    def _extract_state_track_number(self, response):
        return response.json()['trackNo']

    def get_track_number(self, device_name):
        query_url = self._generate_state_query(device_name)
        response = self._process_query(query_url, True)
        return self._extract_state_track_number(response)

    def _process_query(self, query_url, return_response=False):
        response = requests.get(query_url)
        if response.ok:
            if return_response:
                return response
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

    def previous_track(self, device):
        room_name = device.name
        if self.get_track_number(room_name) == 1:
            restart_song_query = self._generate_track_seek_query(room_name, 1)
            return self._process_query(restart_song_query)
        query_url = self._generate_previous_track_query(room_name)
        return self._process_query(query_url)

    def get_track_info(self, device):
        room_name = device.name
        state_query = self._generate_state_query(room_name)
        response = self._process_query(state_query, True)
        current_track = response.json()['currentTrack']
        track = Track("", current_track['title'])
        artist = Artist("", current_track['artist'])
        return track, artist
