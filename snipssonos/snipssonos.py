from skill import MusicPlayerSkill
from services.node_music_playback import SonosMusicPlaybackService
from services.node_device_discovery import NodeDeviceDiscoveryService

class SonosMusicPlayerSkill(MusicPlayerSkill):
    def __init__(self):
        self.music_playback_service = SonosMusicPlaybackService()
        self.device_discovery_service = NodeDeviceDiscoveryService()

    def speaker_interrupt(self):
        self.music_playback_service.pause(self.device_discovery_service.get_device().name)

    def resume_music(self):
        self.music_playback_service.resume(self.device_discovery_service.get_device().name)

    def previous_song(self):
        self.music_playback_service.previous_song(self.device_discovery_service.get_device().name)

    def next_song(self):
        self.music_playback_service.next_song(self.device_discovery_service.get_device().name)
