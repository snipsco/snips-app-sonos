# -*-: coding utf-8 -*-
""" Sonos skill for Snips. """

from __future__ import unicode_literals

import soco
import time

from provider.local_player import LocalPlayer
from provider.tune_in_player import TuneInPlayer
from provider.spotify_player import SpotifyPlayer
from provider.provider_player_template import ProviderPlayerTemplate

MAX_VOLUME = 70
GAIN = 4


class SnipsSonos:
    """ Sonos skill for Snips. """

    def __init__(self, spotify_refresh_token=None, speaker_index=None, locale=None, sonos_ip=None):
        # if ip is provided try to connect
        if sonos_ip is not None:
                self.device = soco.core.SoCo(sonos_ip)
        else:
            # discover the device
            devices = soco.discover()
            if devices is None or len(list(devices)) == 0:
                time.sleep(1)
                devices = soco.discover()
            if devices is None or len(list(devices)) == 0:
                self.device = None
                return
            try:
                speaker_index = int(speaker_index)
            except Exception:
                speaker_index = 0
            if speaker_index >= len(list(devices)):
                speaker_index = 0
            self.device = list(devices)[speaker_index]
        self.providerPlayers = [
            TuneInPlayer(),
            LocalPlayer(self.device),
            SpotifyPlayer()
        ]
        self.max_volume = MAX_VOLUME
        self.previous_volume = None

        # include option to use local library

    def pause_sonos(self):
        if self.device is None:
            return
        self.device.pause()

    def volume_up(self, level):
        if self.device is None:
            return
        level = int(level) if level is not None else 1
        current_volume = self.device.volume
        self.device.volume = min(
            current_volume + GAIN * level,
            self.max_volume)
        self.device.play()

    def volume_down(self, level):
        if self.device is None:
            return
        level = int(level) if level is not None else 1
        self.device.volume -= GAIN * level
        self.device.play()
        print(self.device.volume)

    def set_volume(self, volume_value):
        if self.device is None:
            return
        self.device.volume = volume_value
        self.device.play()

    def set_to_low_volume(self):
        if self.device.get_current_transport_info()['current_transport_state'] != "PLAYING":
            return None
        if self.device is None:
            return
        self.previous_volume = self.device.volume
        self.device.volume = min(6, self.device.volume)
        self.device.play()

    def set_to_previous_volume(self):
        if self.device is None:
            return
        if self.previous_volume is None:
            return None
        self.device.volume = self.previous_volume
        if self.device.get_current_transport_info()['current_transport_state'] == "PLAYING":
            self.device.play()

    def stop_sonos(self):
        if self.device is None:
            return
        self.device.stop()

    def play_template(self, name, shuffle=False, func_name=None):
        if self.device is None:
            return
        for provider in self.providerPlayers:
            func = getattr(provider, func_name)
            if func(self.device, name, shuffle):
                print("playing playlist:%s" % name)
                return

    def turn_on_radio(self, radio_name):
        self.play_template(radio_name, func_name="play_station")

    def play_playlist(self, name, _shuffle=False):
        self.play_template(name, _shuffle, "play_playlist")

    def play_artist(self, name):
        self.play_template(name, func_name= "play_artist")

    def play_album(self, name, _shuffle=False):
        self.play_template(name, func_name= "play_album")

    def play_song(self, name):
        self.play_template(name, func_name= "play_track")

    def play_next_item_in_queue(self):
        if self.device is None:
            return
        try:
            self.device.next()
        except Exception:
            print("Failed to play next item, maybe last song?")

    def play_previous_item_in_queue(self):
        if self.device is None:
            return
        try:
            self.device.previous()
        except Exception:
            print("Failed to play previous item, maybe first song?")


    def get_info(self):
        # Get info about currently playing tune
        info = self.device.get_current_track_info()
        return info['title'], info['artist'], info['album']

    def add_song(self):
        # Save song in spotify
        title, artist, _ = self.get_info()
        self.spotify.add_song(artist, title)

    def play(self):
        # Save song in spotify
        self.device.play()
