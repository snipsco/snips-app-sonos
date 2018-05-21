from device_discovery import DeviceDiscoveryService
from snipssonos.adapters.sonos_node_api import SonosNodeAPIClient as player

class MusicPlaybackService(object):
    """
    This class describes the API to interact with the Music Playback service.
    """
    def __init__(self, device_discovery_service):
        self.device_discovery_service = device_discovery_service
        self.player = None

    def pause(self):
        device = self.device_discovery_service.get()
        response_object = self.player.to_device(device).execute("pause")
        return response_object

    def next_song(self):
        pass

    def previous(self):
        pass

    def play(self):
        pass

    def volume_down(self, level):
        pass

    def volume_up(self, level):
        pass

    def set_volume(self, level):
        pass



