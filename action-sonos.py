#!/usr/bin/env python2
# -*-: coding utf-8 -*-

import ConfigParser
import io
import traceback

from hermes_python.hermes import Hermes
from hermes_python.ontology import *

from snipssonos.snipssonos import SonosControllerAction
from snipssonos.use_cases.volume_up import VolumeUpUseCase
from snipssonos.use_cases.volume_down import VolumeDownUseCase
from snipssonos.use_cases.volume_set import VolumeSetUseCase
from snipssonos.use_cases.play_track import PlayTrackUseCase
from snipssonos.use_cases.play_artist import PlayArtistUseCase
from snipssonos.use_cases.resume_music import ResumeMusicUseCase
from snipssonos.use_cases.speaker_interrupt import SpeakerInterruptUseCase
from snipssonos.adapters.request_adapter import VolumeUpRequestAdapter, PlayTrackRequestAdapter, \
    PlayArtistRequestAdapter, VolumeSetRequestAdapter, VolumeDownRequestAdapter, ResumeMusicRequestAdapter, \
    SpeakerInterruptRequestAdapter
from snipssonos.services.node_device_discovery_service import NodeDeviceDiscoveryService
from snipssonos.services.node_device_transport_control import NodeDeviceTransportControlService
from snipssonos.services.node_music_playback_service import NodeMusicPlaybackService
from snipssonos.services.spotify_music_search_service import SpotifyMusicSearchService

# Utils functions
CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

HOSTNAME = "raspi-dev-antho.local"

HERMES_HOST = "{}:1883".format(HOSTNAME)
MOPIDY_HOST = HOSTNAME


class SnipsConfigParser(ConfigParser.SafeConfigParser):
    def to_dict(self):
        return {section: {option_name: option for option_name, option in self.items(section)} for section in
                self.sections()}


def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, ConfigParser.Error) as e:
        return dict()

# Music management functions

def addSong_callback(hermes, intentMessage):
    hermes.action.add_song()

def getInfos_callback(hermes, intentMessage):
    hermes.action.get_infos()

def playAlbum_callback(hermes, intentMessage):
    hermes.action.play_album(intentMessage.slots.album_name, intentMessage.slots.album_lecture_mode)

def playArtist_callback(hermes, intentMessage):
    hermes.action.play_artist(intentMessage.slots.artist_name)

def playPlaylist_callback(hermes, intentMessage):
    hermes.action.play_playlist(intentMessage.slots.playlist_name, intentMessage.slots.playlist_lecture_mode)

def playSong_callback(hermes, intentMessage):
    hermes.action.play_song(intentMessage.slots.song_name)

def radioOn_callback(hermes, intentMessage):
    hermes.action.radio_on(intentMessage.slots.radio_name)


# Playback functions

#P0
def previousSong_callback(hermes, intentMessage):
    hermes.action.previous_song()

#P0
def nextSong_callback(hermes, intentMessage):
    hermes.action.next_song()

#P0
def resumeMusic_callback(hermes, intentMessage):
    hermes.action.resume_music()

#P0
def speakerInterrupt_callback(hermes, intentMessage):
    hermes.action.speaker_interrupt()


def volumeDown_callback(hermes, intentMessage):
    hermes.action.volume_down(intentMessage.slots.volume_lower)

def volumeUp_callback(hermes, intentMessage):
    hermes.action.volume_up(intentMessage.slots.volume_higher)


if __name__ == "__main__":

    with Hermes(HERMES_HOST) as h:

        h.action = SonosControllerAction()

        h\
            .subscribe_intent("volumeUp", volumeUp_callback) \
            .subscribe_intent("previousSong", previousSong_callback) \
            .subscribe_intent("playSong", playSong_callback) \
            .subscribe_intent("playArtist", playArtist_callback) \
            .subscribe_intent("getInfos", getInfos_callback) \
            .subscribe_intent("speakerInterrupt", speakerInterrupt_callback) \
            .subscribe_intent("resumeMusic", resumeMusic_callback) \
            .subscribe_intent("addSong", addSong_callback) \
            .subscribe_intent("nextSong", nextSong_callback) \
            .subscribe_intent("radioOn", radioOn_callback) \
            .subscribe_intent("playAlbum", playAlbum_callback) \
            .subscribe_intent("volumeDown", volumeDown_callback) \
            .subscribe_intent("playPlaylist", playPlaylist_callback) \
            .loop_forever()
