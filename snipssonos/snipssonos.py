# -*-: coding utf-8 -*-
""" Sonos skill for Snips. """

from __future__ import unicode_literals

import soco
import time

from random import shuffle

from soco.music_services import MusicService
from soco.data_structures import DidlItem, DidlResource
from soco.compat import quote_url

from .spotify import SpotifyClient

MAX_VOLUME = 70
GAIN = 4


class SnipsSonos:
    """ Sonos skill for Snips. """

    def __init__(self, spotify_refresh_token=None, speaker_index=None):
        # find the device
        devices = soco.discover()
        if devices is None or len(list(devices)) == 0:
            time.sleep(1)
            devices = soco.discover()
        if devices is None or len(list(devices)) == 0:
            return
        try:
            speaker_index = int(speaker_index)
        except Exception:
            speaker_index = 0
        if speaker_index >= len(list(devices)):
            speaker_index = 0
        self.device = list(devices)[speaker_index]
        try:
            self.tunein_service = MusicService('TuneIn')
        except Exception:
            self.tunein_service = None
        try:
            self.spotify_service = MusicService('Spotify')
        except Exception:
            self.spotify_service = None
        self.max_volume = MAX_VOLUME
        if spotify_refresh_token is not None:
            self.spotify = SpotifyClient(spotify_refresh_token)
        self.previous_volume = None

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
        print self.device.volume

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

    def turn_on_radio(self, radio_name):
        if self.device is None:
            return None
        if self.tunein_service is None:
            return None
        res = self.tunein_service.search('stations', term=radio_name)
        if 'mediaMetadata' not in res:
            return "radio not found"
        if isinstance(res['mediaMetadata'], list):
            radio_id = res['mediaMetadata'][0]['id']
        elif isinstance(res['mediaMetadata'], dict):
            radio_id = res['mediaMetadata']['id']
        else:
            raise TypeError("Unknown type for tune in search metadata")
        radio_uri = self.tunein_service.get_media_uri(radio_id)
        try:
            self.device.play_uri(radio_uri.replace('http', 'x-rincon-mp3radio'))
        except Exception:
            # unknown problem playing radio uri...
            return None

    def play_playlist(self, name, _shuffle=False):
        if self.device is None:
            return
        if self.spotify is None:
            return
        tracks = self.spotify.get_tracks_from_playlist(name)
        if tracks is None:
            return None
        self.device.stop()
        self.device.clear_queue()
        if _shuffle:
            shuffle(tracks)
        for track in tracks:
            self.add_from_service(track['track']['uri'], self.spotify_service, True)
        self.device.play_from_queue(0)

    def play_artist(self, name):
        if self.device is None:
            return
        if self.spotify is None:
            return
        tracks = self.spotify.get_top_tracks_from_artist(name)
        if tracks is None:
            return None
        self.device.stop()
        self.device.clear_queue()
        for track in tracks:
            self.add_from_service(track['uri'], self.spotify_service, True)
        self.device.play_from_queue(0)

    def play_album(self, album, _shuffle=False):
        if self.device is None:
            return
        if self.spotify is None:
            return
        tracks = self.spotify.get_tracks_from_album(album)
        if tracks is None:
            return None
        self.device.stop()
        self.device.clear_queue()
        if _shuffle:
            shuffle(tracks)
        for track in tracks:
            self.add_from_service(track['uri'], self.spotify_service, True)
        self.device.play_from_queue(0)

    def play_song(self, name):
        if self.device is None:
            return
        if self.spotify is None:
            return
        track = self.spotify.get_track(name)
        if track is None:
            return None
        self.device.stop()
        self.device.clear_queue()
        self.add_from_service(track['uri'], self.spotify_service, True)
        self.device.play_from_queue(0)

    def play_next_item_in_queue(self):
        if self.device is None:
            return
        try:
            self.device.next()
        except Exception:
            print "Failed to play next item, maybe last song?"

    def play_previous_item_in_queue(self):
        if self.device is None:
            return
        try:
            self.device.previous()
        except Exception:
            print "Failed to play previous item, maybe first song?"

    def add_from_service(self, item_id, service, is_track=True):
        # The DIDL item_id is made of the track_id (url escaped), but with an 8
        # (hex) digit prefix. It is not clear what this is for, but it doesn't
        # seem to matter (too much) what it is. We can use junk (thought the
        # first digit must be 0 or 1), and the player seems to do the right
        # thing. Real DIDL items sent to a player also have a title and a
        # parent_id (usually the id of the relevant album), but they are not
        # necessary. The flow charts at http://musicpartners.sonos.com/node/421
        # and http://musicpartners.sonos.com/node/422 suggest that it is the job
        # of the player, not the controller, to call get_metadata with a track
        # id, so this might explain why no metadata is needed at this stage.

        # NB: quote_url will break if given unicode on Py2.6, and early 2.7. So
        # we need to encode.

        if self.device is None:
            return

        item_id = quote_url(item_id.encode('utf-8'))
        didl_item_id = "0fffffff{0}".format(item_id)

        # For an album:
        if not is_track:
            uri = 'x-rincon-cpcontainer:' + didl_item_id

        else:
            # For a track:
            uri = service.sonos_uri_from_id(item_id)

        res = [DidlResource(uri=uri, protocol_info="Snips")]
        didl = DidlItem(
            title="Snips",
            # This is ignored. Sonos gets the title from the item_id
            parent_id="Snips",  # Ditto
            item_id=didl_item_id,
            desc=service.desc,
            resources=res)

        self.device.add_to_queue(didl)

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
