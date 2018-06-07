#!/usr/bin/env python2
# -*-: coding utf-8 -*-

import ConfigParser
import io
import traceback

from hermes_python.hermes import Hermes
from hermes_python.ontology import *

from snipssonos.use_cases.volume_up import VolumeUpUseCase
from snipssonos.use_cases.volume_down import VolumeDownUseCase
from snipssonos.use_cases.volume_set import VolumeSetUseCase
from snipssonos.use_cases.mute import MuteUseCase
from snipssonos.use_cases.play_track import PlayTrackUseCase
from snipssonos.use_cases.play_artist import PlayArtistUseCase
from snipssonos.use_cases.resume_music import ResumeMusicUseCase
from snipssonos.use_cases.speaker_interrupt import SpeakerInterruptUseCase
from snipssonos.adapters.request_adapter import VolumeUpRequestAdapter, PlayTrackRequestAdapter, \
    PlayArtistRequestAdapter, VolumeSetRequestAdapter, VolumeDownRequestAdapter, ResumeMusicRequestAdapter, \
    SpeakerInterruptRequestAdapter, MuteRequestAdapter
from snipssonos.services.node_device_discovery_service import NodeDeviceDiscoveryService
from snipssonos.services.node_device_transport_control import NodeDeviceTransportControlService
from snipssonos.services.node_music_playback_service import NodeMusicPlaybackService
from snipssonos.services.spotify_music_search_service import SpotifyMusicSearchService

# Utils functions
CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

HOSTNAME = "sonos-antho.local"

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
    raise NotImplementedError("addSong_callback() not implemented")


def getInfos_callback(hermes, intentMessage):
    raise NotImplementedError("getInfos_callback() not implemented")


def playAlbum_callback(hermes, intentMessage):
    raise NotImplementedError("playAlbum_callback() not implemented")


def playPlaylist_callback(hermes, intentMessage):
    raise NotImplementedError("playPlaylist_callback() not implemented")


def radioOn_callback(hermes, intentMessage):
    raise NotImplementedError("radioOn_callback() not implemented")


def previousSong_callback(hermes, intentMessage):
    raise NotImplementedError("previousSong_callback() not implemented")


def nextSong_callback(hermes, intentMessage):
    raise NotImplementedError("nextSong_callback() not implemented")


def resumeMusic_callback(hermes, intentMessage):  # Playback functions
    usecase = ResumeMusicUseCase(hermes.device_discovery_service, hermes.device_transport_control_service)
    resume_music_request = ResumeMusicRequestAdapter.from_intent_message(intentMessage)

    response = usecase.execute(resume_music_request)
    if not response:
        print response.value
        hermes.publish_end_session(intentMessage.session_id, "An error occured.")
    else:
        print response
        hermes.publish_end_session(intentMessage.session_id, "")


def speakerInterrupt_callback(hermes, intentMessage):
    usecase = SpeakerInterruptUseCase(hermes.device_discovery_service, hermes.device_transport_control_service)
    speaker_interrupt_request = SpeakerInterruptRequestAdapter.from_intent_message(intentMessage)

    response = usecase.execute(speaker_interrupt_request)
    if not response:
        print response.value
        hermes.publish_end_session(intentMessage.session_id, "An error occured.")
    else:
        print response
        hermes.publish_end_session(intentMessage.session_id, "")


def volumeDown_callback(hermes, intentMessage):
    usecase = VolumeDownUseCase(hermes.device_discovery_service, hermes.device_transport_control_service)
    volume_down_request = VolumeDownRequestAdapter.from_intent_message(intentMessage)

    response = usecase.execute(volume_down_request)
    if not response:
        print response.value
        hermes.publish_end_session(intentMessage.session_id, "An error occured.")
    else:
        print response
        hermes.publish_end_session(intentMessage.session_id, "")


def volumeUp_callback(hermes, intentMessage):
    usecase = VolumeUpUseCase(hermes.device_discovery_service, hermes.device_transport_control_service)
    volume_up_request = VolumeUpRequestAdapter.from_intent_message(intentMessage)

    response = usecase.execute(volume_up_request)
    if not response:
        print response.value
        hermes.publish_end_session(intentMessage.session_id, "An error occured.")
    else:
        print response
        hermes.publish_end_session(intentMessage.session_id, "")


def volumeSet_callback(hermes, intentMessage):
    usecase = VolumeSetUseCase(hermes.device_discovery_service, hermes.device_transport_control_service)
    volume_set_request = VolumeSetRequestAdapter.from_intent_message(intentMessage)

    response = usecase.execute(volume_set_request)
    if not response:
        print response.value
        hermes.publish_end_session(intentMessage.session_id, "An error occured.")
    else:
        print response
        hermes.publish_end_session(intentMessage.session_id, "")


def mute_callback(hermes, intentMessage):
    usecase = MuteUseCase(hermes.device_discovery_service, hermes.device_transport_control_service)
    mute_request = MuteRequestAdapter.from_intent_message(intentMessage)

    response = usecase.execute(mute_request)
    if not response:
        print response.value
        hermes.publish_end_session(intentMessage.session_id, "An error occured.")
    else:
        print response
        hermes.publish_end_session(intentMessage.session_id, "")


def playSong_callback(hermes, intentMessage):
    use_case = PlayTrackUseCase(hermes.device_discovery_service, hermes.music_search_service,
                                hermes.music_playback_service)
    play_track_request = PlayTrackRequestAdapter.from_intent_message(intentMessage)

    response = use_case.execute(play_track_request)

    if not response:
        print response.value
        hermes.publish_end_session(intentMessage.session_id, "An error occured")
    else:
        print response
        hermes.publish_end_session(intentMessage.session_id, "")


def playArtist_callback(hermes, intentMessage):
    use_case = PlayArtistUseCase(hermes.device_discovery_service, hermes.music_search_service,
                                 hermes.music_playback_service)
    play_artist_request = PlayArtistRequestAdapter.from_intent_message(intentMessage)

    print play_artist_request
    response = use_case.execute(play_artist_request)

    if not response:
        print response.value
        hermes.publish_end_session(intentMessage.session_id, "An error occured")
    else:
        print response
        hermes.publish_end_session(intentMessage.session_id, "")


if __name__ == "__main__":
    configuration = read_configuration_file("config.ini")
    client_id = configuration['secret']['client_id']
    client_secret = configuration['secret']['client_secret']

    with Hermes(HERMES_HOST) as h:
        h.device_discovery_service = NodeDeviceDiscoveryService()
        h.device_transport_control_service = NodeDeviceTransportControlService()
        h.music_search_service = SpotifyMusicSearchService(client_id, client_secret)
        h.music_playback_service = NodeMusicPlaybackService()

        h \
            .subscribe_intent("playMusic3", playArtist_callback) \
            .subscribe_intent("volumeUp3", volumeUp_callback) \
            .subscribe_intent("volumeDown3", volumeDown_callback) \
            .subscribe_intent("volumeSet3", volumeSet_callback) \
            .subscribe_intent("muteSound3", mute_callback) \
            .subscribe_intent("resumeMusic", resumeMusic_callback) \
            .subscribe_intent("speakerInterrupt", speakerInterrupt_callback) \
            .loop_forever()
