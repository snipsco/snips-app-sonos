import json
import requests

PROTOCOL = "http"
HOST = "localhost"
PORT = 5005

from music_playback import MusicPlaybackService
from snipssonos.adapters.sonos_node_api import SonosNodeAPIClient as client

from snipssonos.exceptions import APIRequestWrongParams

class NodeMusicPlaybackService(MusicPlaybackService):
    def __init__(self, device_discovery_service):
        super(NodeMusicPlaybackService, self).__init__(device_discovery_service)
        self.player = client()
