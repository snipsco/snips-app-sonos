#!/usr/bin/env python2
# -*-: coding utf-8 -*-

import logging

from hermes_python.hermes import Hermes

from snipssonos.helpers.snips_config_parser import read_configuration_file
from snipssonos.use_cases.volume.up import VolumeUpUseCase
from snipssonos.use_cases.volume.down import VolumeDownUseCase
from snipssonos.use_cases.volume.set import VolumeSetUseCase
from snipssonos.use_cases.mute import MuteUseCase
from snipssonos.use_cases.play.track import PlayTrackUseCase
from snipssonos.use_cases.play.artist import PlayArtistUseCase
from snipssonos.use_cases.play.music import PlayMusicUseCase
from snipssonos.use_cases.resume_music import ResumeMusicUseCase
from snipssonos.use_cases.speaker_interrupt import SpeakerInterruptUseCase

from snipssonos.adapters.request_adapter import VolumeUpRequestAdapter, PlayTrackRequestAdapter, \
    PlayArtistRequestAdapter, VolumeSetRequestAdapter, VolumeDownRequestAdapter, ResumeMusicRequestAdapter, \
    SpeakerInterruptRequestAdapter, MuteRequestAdapter, PlayMusicRequestAdapter
from snipssonos.services.node.device_discovery_service import NodeDeviceDiscoveryService
from snipssonos.services.node.device_transport_control import NodeDeviceTransportControlService
from snipssonos.services.node.music_playback_service import NodeMusicPlaybackService
from snipssonos.services.spotify.music_search_service import SpotifyMusicSearchService

from snipssonos.adapters.tts_sentence_adapter import TTSSentenceGenerator

from snipssonos.shared.feedback import FR_TTS_SHORT_ERROR

# Utils functions
CONFIG_INI = "config.ini"

HOSTNAME = "localhost"

HERMES_HOST = "{}:1883".format(HOSTNAME)
MOPIDY_HOST = HOSTNAME

# Config & Logging
CONFIGURATION = read_configuration_file("config.ini")
LOG_LEVEL = CONFIGURATION['global']['log_level']
if LOG_LEVEL == "info":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
elif LOG_LEVEL == "debug":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
else:
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


# Music management functions
def addSong_callback(hermes, intentMessage):
    raise NotImplementedError("addSong_callback() not implemented")


def getInfos_callback(hermes, intentMessage):
    raise NotImplementedError("getInfos_callback() not implemented")


def radioOn_callback(hermes, intentMessage):
    raise NotImplementedError("radioOn_callback() not implemented")


def previousSong_callback(hermes, intentMessage):
    raise NotImplementedError("previousSong_callback() not implemented")


def nextSong_callback(hermes, intentMessage):
    pass


def resumeMusic_callback(hermes, intentMessage):  # Playback functions
    use_case = ResumeMusicUseCase(hermes.device_discovery_service, hermes.device_transport_control_service)
    resume_music_request = ResumeMusicRequestAdapter.from_intent_message(intentMessage)

    response = use_case.execute(resume_music_request)
    if not response:
        logging.info(response.value)
        hermes.publish_end_session(intentMessage.session_id, FR_TTS_SHORT_ERROR)
    else:
        logging.info(response)
        hermes.publish_end_session(intentMessage.session_id, "")


def speakerInterrupt_callback(hermes, intentMessage):
    use_case = SpeakerInterruptUseCase(hermes.device_discovery_service, hermes.device_transport_control_service)
    speaker_interrupt_request = SpeakerInterruptRequestAdapter.from_intent_message(intentMessage)

    response = use_case.execute(speaker_interrupt_request)
    if not response:
        logging.info(response.value)
        hermes.publish_end_session(intentMessage.session_id, FR_TTS_SHORT_ERROR)
    else:
        logging.info(response)
        hermes.publish_end_session(intentMessage.session_id, "")


def volumeDown_callback(hermes, intentMessage):
    use_case = VolumeDownUseCase(hermes.device_discovery_service, hermes.device_transport_control_service)
    volume_down_request = VolumeDownRequestAdapter.from_intent_message(intentMessage)

    response = use_case.execute(volume_down_request)
    if not response:
        logging.info(response.value)
        hermes.publish_end_session(intentMessage.session_id, FR_TTS_SHORT_ERROR)
    else:
        logging.info(response)
        hermes.publish_end_session(intentMessage.session_id, "")


def volumeUp_callback(hermes, intentMessage):
    use_case = VolumeUpUseCase(hermes.device_discovery_service, hermes.device_transport_control_service)
    volume_up_request = VolumeUpRequestAdapter.from_intent_message(intentMessage)

    response = use_case.execute(volume_up_request)
    if not response:
        logging.info(response.value)
        hermes.publish_end_session(intentMessage.session_id, FR_TTS_SHORT_ERROR)
    else:
        logging.info(response)
        hermes.publish_end_session(intentMessage.session_id, "")


def volumeSet_callback(hermes, intentMessage):
    use_case = VolumeSetUseCase(hermes.device_discovery_service, hermes.device_transport_control_service)
    volume_set_request = VolumeSetRequestAdapter.from_intent_message(intentMessage)

    response = use_case.execute(volume_set_request)
    if not response:
        logging.info(response.value)
        hermes.publish_end_session(intentMessage.session_id, FR_TTS_SHORT_ERROR)
    else:
        logging.info(response)
        hermes.publish_end_session(intentMessage.session_id, "")


def mute_callback(hermes, intentMessage):
    use_case = MuteUseCase(hermes.device_discovery_service, hermes.device_transport_control_service)
    mute_request = MuteRequestAdapter.from_intent_message(intentMessage)

    response = use_case.execute(mute_request)
    if not response:
        logging.info(response.value)
        hermes.publish_end_session(intentMessage.session_id, FR_TTS_SHORT_ERROR)
    else:
        logging.info(response)
        hermes.publish_end_session(intentMessage.session_id, "")


def playTrack_callback(hermes, intentMessage):
    use_case = PlayTrackUseCase(hermes.device_discovery_service, hermes.music_search_service,
                                hermes.music_playback_service)
    play_track_request = PlayTrackRequestAdapter.from_intent_message(intentMessage)

    response = use_case.execute(play_track_request)

    if not response:
        logging.info(response.value)
        hermes.publish_end_session(intentMessage.session_id, FR_TTS_SHORT_ERROR)
    else:
        logging.info(response)
        hermes.publish_end_session(intentMessage.session_id, "")


def playArtist_callback(hermes, intentMessage):
    use_case = PlayArtistUseCase(hermes.device_discovery_service, hermes.music_search_service,
                                 hermes.music_playback_service)
    play_artist_request = PlayArtistRequestAdapter.from_intent_message(intentMessage)

    logging.info(play_artist_request)
    response = use_case.execute(play_artist_request)

    if not response:
        logging.info(response.value)
        hermes.publish_end_session(intentMessage.session_id, FR_TTS_SHORT_ERROR)
    else:
        logging.info(response)
        hermes.publish_end_session(intentMessage.session_id, "")


def playMusic_callback(hermes, intentMessage):
    use_case = PlayMusicUseCase(hermes.device_discovery_service, hermes.music_search_service,
                                hermes.music_playback_service)
    play_music_request = PlayMusicRequestAdapter.from_intent_message(intentMessage)

    response = use_case.execute(play_music_request)

    if not response:
        logging.error('Error type : {}'.format(response.type))
        logging.error('Error message : {}'.format(response.message))
        logging.error('Error exception : {}'.format(response.exception))

        feedback = TTSSentenceGenerator("FRENCH").from_response_object(response)
        hermes.publish_end_session(intentMessage.session_id, feedback)
    else:
        logging.debug("Response Success : {}".format(response))
        hermes.publish_end_session(intentMessage.session_id, response.feedback)


if __name__ == "__main__":
    client_id = CONFIGURATION['secret']['client_id']
    client_secret = CONFIGURATION['secret']['client_secret']
    refresh_token = CONFIGURATION['secret']['refresh_token']

    with Hermes(HERMES_HOST) as h:
        h.device_discovery_service = NodeDeviceDiscoveryService()
        h.device_transport_control_service = NodeDeviceTransportControlService()
        h.music_search_service = SpotifyMusicSearchService(client_id, client_secret, refresh_token)
        h.music_playback_service = NodeMusicPlaybackService()
        h \
            .subscribe_intent("playMusic4", playMusic_callback) \
            .subscribe_intent("volumeUp4", volumeUp_callback) \
            .subscribe_intent("volumeDown4", volumeDown_callback) \
            .subscribe_intent("volumeSet4", volumeSet_callback) \
            .subscribe_intent("muteSound4", mute_callback) \
            .subscribe_intent("resumeMusic4", resumeMusic_callback) \
            .subscribe_intent("speakerInterrupt4", speakerInterrupt_callback) \
            .subscribe_intent("nextSong4", nextSong_callback) \
            .loop_forever()
