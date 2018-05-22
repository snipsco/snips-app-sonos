# -*- coding: utf-8 -*-

from shared.skill import MusicPlayerSkill
from services.node_music_playback import NodeMusicPlaybackService
from services.node_device_discovery import NodeDeviceDiscoveryService

class SonosMusicPlayerSkill(MusicPlayerSkill): # This is the controller basically.
    def __init__(self):
        self.device_discovery_service = NodeDeviceDiscoveryService()
        self.music_playback_service = NodeMusicPlaybackService(self.device_discovery_service)

    def speaker_interrupt(self, request):
        self.music_playback_service.pause()

    def resume_music(self, request):
        self.music_playback_service.resume()

    def previous_song(self, request):
        self.music_playback_service.previous_song()

    def next_song(self, request):
        self.music_playback_service.next_song()

