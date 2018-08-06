#!/usr/bin/env python2
# -*-: coding utf-8 -*-

import logging
import sys
import traceback

from hermes_python.hermes import Hermes

from snipssonos.helpers.snips_config_parser import read_configuration_file
from snipssonos.helpers.snips_configuration_validator import validate_configuration_file, AVAILABLE_MUSIC_SERVICES
from snipssonos.use_cases.hotword.lower_volume import HotwordLowerVolumeUseCase
from snipssonos.use_cases.hotword.restore_volume import HotwordRestoreVolumeUseCase
from snipssonos.use_cases.volume.up import VolumeUpUseCase
from snipssonos.use_cases.volume.down import VolumeDownUseCase
from snipssonos.use_cases.volume.set import VolumeSetUseCase
from snipssonos.use_cases.mute import MuteUseCase
from snipssonos.use_cases.play.track import PlayTrackUseCase
from snipssonos.use_cases.play.artist import PlayArtistUseCase
from snipssonos.use_cases.play.music import PlayMusicUseCase
from snipssonos.use_cases.resume_music import ResumeMusicUseCase
from snipssonos.use_cases.speaker_interrupt import SpeakerInterruptUseCase
from snipssonos.use_cases.next_track import NextTrackUseCase
from snipssonos.use_cases.previous_track import PreviousTrackUseCase
from snipssonos.use_cases.get_track_info import GetTrackInfoUseCase

from snipssonos.use_cases.request_objects import HotwordLowerVolumeRequestObject, HotwordRestoreVolumeRequestObject
from snipssonos.adapters.request_adapter import VolumeUpRequestAdapter, PlayTrackRequestAdapter, \
    PlayArtistRequestAdapter, VolumeSetRequestAdapter, VolumeDownRequestAdapter, ResumeMusicRequestAdapter, \
    SpeakerInterruptRequestAdapter, MuteRequestAdapter, PlayMusicRequestAdapter, NextTrackRequestAdapter, \
    PreviousTrackRequestAdapter, GetTrackInfoRequestAdapter
from snipssonos.services.node.device_discovery_service import NodeDeviceDiscoveryService
from snipssonos.services.node.device_transport_control import NodeDeviceTransportControlService
from snipssonos.services.spotify.music_playback_service import SpotifyNodeMusicPlaybackService
from snipssonos.services.deezer.music_playback_service import DeezerNodeMusicPlaybackService
from snipssonos.services.spotify.music_search_service import SpotifyMusicSearchService
from snipssonos.services.hermes.state_persistence import HermesStatePersistence
from snipssonos.services.feedback.feedback_service import FeedbackService

from snipssonos.services.deezer.music_search_and_play_service import DeezerMusicSearchService

# Utils functions
CONFIG_INI = "config.ini"


# Configuration
CONFIGURATION = read_configuration_file(CONFIG_INI)
validate_configuration_file(CONFIGURATION)

MUSIC_PROVIDER = CONFIGURATION["global"].get('music_provider', AVAILABLE_MUSIC_SERVICES[0])
CLIENT_ID = CONFIGURATION['secret']['client_id']
CLIENT_SECRET = CONFIGURATION['secret']['client_secret']
REFRESH_TOKEN = CONFIGURATION['secret']['refresh_token']
# Connection
HOSTNAME = CONFIGURATION['global'].get('hostname', "localhost")
HERMES_HOST = "{}:1883".format(HOSTNAME)
# Language
LANGUAGE = CONFIGURATION['global'].get('language', "fr")

# Logging
LOG_LEVEL = CONFIGURATION['global']['log_level']
if LOG_LEVEL == "info":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
elif LOG_LEVEL == "debug":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
else:
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')



# Hotword callback
def hotword_detected_callback(hermes, sessionStartedMessage):
    use_case = HotwordLowerVolumeUseCase(hermes.device_discovery_service, hermes.device_transport_control_service,
                                         hermes.state_persistence_service)
    request_object = HotwordLowerVolumeRequestObject()

    response = use_case.execute(request_object)
    if not response:
        logging.error("An error occured when trying to lower the volume when the wakeword was detected")
        hermes.publish_end_session(sessionStartedMessage.session_id, "")


def restore_volume_for_hotword(intent_callback):
    def restore_volume_wrapper(hermes, intentMessage):
        intent_callback(hermes, intentMessage)  # We call the callback

        # We restore the volume to what it was before the hotword was detected.
        use_case = HotwordRestoreVolumeUseCase(hermes.device_discovery_service, hermes.device_transport_control_service,
                                               hermes.state_persistence_service)
        request_object = HotwordRestoreVolumeRequestObject()
        response = use_case.execute(request_object)

        if not response:
            logging.error("Error when recovering the volume")
            logging.error(response.message)

    return restore_volume_wrapper


def session_ended_callback(hermes, sessionEndedMessage):
    INTENT_NOT_RECOGNIZED = 4  # TODO : refactor this.
    # We restore the volume to what it was before the hotword was detected.
    if sessionEndedMessage.termination.termination_type == INTENT_NOT_RECOGNIZED:
        use_case = HotwordRestoreVolumeUseCase(hermes.device_discovery_service, hermes.device_transport_control_service,
                                               hermes.state_persistence_service)
        request_object = HotwordRestoreVolumeRequestObject()
        response = use_case.execute(request_object)

        if not response:
            logging.error("Error when recovering the volume")
            logging.error(response.message)


# Music management functions
@restore_volume_for_hotword
def addSong_callback(hermes, intentMessage):
    raise NotImplementedError("addSong_callback() not implemented")


@restore_volume_for_hotword
def getInfos_callback(hermes, intentMessage):
    use_case = GetTrackInfoUseCase(hermes.device_discovery_service,
                                   hermes.device_transport_control_service, hermes.feedback_service)
    get_track_request = GetTrackInfoRequestAdapter.from_intent_message(intentMessage)

    response = use_case.execute(get_track_request)

    if not response:
        feedback = hermes.feedback_service.from_response_object(response)
        hermes.publish_end_session(intentMessage.session_id, feedback)
    else:
        logging.debug("Response Success : {}".format(response))
        hermes.publish_end_session(intentMessage.session_id, response.feedback)


@restore_volume_for_hotword
def radioOn_callback(hermes, intentMessage):
    raise NotImplementedError("radioOn_callback() not implemented")


@restore_volume_for_hotword
def previousSong_callback(hermes, intentMessage):
    use_case = PreviousTrackUseCase(hermes.device_discovery_service, hermes.device_transport_control_service)
    previous_track_request = PreviousTrackRequestAdapter.from_intent_message(intentMessage)

    response = use_case.execute(previous_track_request)
    if not response:
        logging.info(response.value)
        hermes.publish_end_session(intentMessage.session_id, hermes.feedback_service.get_short_error_message())
    else:
        logging.info(response)
        hermes.publish_end_session(intentMessage.session_id, "")


@restore_volume_for_hotword
def nextSong_callback(hermes, intentMessage):
    use_case = NextTrackUseCase(hermes.device_discovery_service, hermes.device_transport_control_service)
    next_track_request = NextTrackRequestAdapter.from_intent_message(intentMessage)

    response = use_case.execute(next_track_request)
    if not response:
        logging.info(response.value)
        hermes.publish_end_session(intentMessage.session_id, hermes.feedback_service.get_short_error_message())
    else:
        logging.info(response)
        hermes.publish_end_session(intentMessage.session_id, "")


@restore_volume_for_hotword
def resumeMusic_callback(hermes, intentMessage):  # Playback functions
    use_case = ResumeMusicUseCase(hermes.device_discovery_service, hermes.device_transport_control_service)
    resume_music_request = ResumeMusicRequestAdapter.from_intent_message(intentMessage)

    response = use_case.execute(resume_music_request)
    if not response:
        logging.info(response.value)
        hermes.publish_end_session(intentMessage.session_id, hermes.feedback_service.get_short_error_message())
    else:
        logging.info(response)
        hermes.publish_end_session(intentMessage.session_id, "")


@restore_volume_for_hotword
def speakerInterrupt_callback(hermes, intentMessage):
    use_case = SpeakerInterruptUseCase(hermes.device_discovery_service, hermes.device_transport_control_service)
    speaker_interrupt_request = SpeakerInterruptRequestAdapter.from_intent_message(intentMessage)

    response = use_case.execute(speaker_interrupt_request)
    if not response:
        logging.info(response.value)
        hermes.publish_end_session(intentMessage.session_id, hermes.feedback_service.get_short_error_message())
    else:
        logging.info(response)
        hermes.publish_end_session(intentMessage.session_id, "")


@restore_volume_for_hotword
def volumeDown_callback(hermes, intentMessage):
    use_case = VolumeDownUseCase(hermes.device_discovery_service, hermes.device_transport_control_service,
                                 hermes.state_persistence_service)
    volume_down_request = VolumeDownRequestAdapter.from_intent_message(intentMessage)

    response = use_case.execute(volume_down_request)
    if not response:
        logging.info(response.value)
        hermes.publish_end_session(intentMessage.session_id, hermes.feedback_service.get_short_error_message())
    else:
        logging.info(response)
        hermes.publish_end_session(intentMessage.session_id, "")


@restore_volume_for_hotword
def volumeUp_callback(hermes, intentMessage):
    use_case = VolumeUpUseCase(hermes.device_discovery_service, hermes.device_transport_control_service,
                               hermes.state_persistence_service)
    volume_up_request = VolumeUpRequestAdapter.from_intent_message(intentMessage)

    response = use_case.execute(volume_up_request)
    if not response:
        logging.info(response.value)
        hermes.publish_end_session(intentMessage.session_id, hermes.feedback_service.get_short_error_message())
    else:
        logging.info(response)
        hermes.publish_end_session(intentMessage.session_id, "")


def volumeSet_callback(hermes, intentMessage):
    use_case = VolumeSetUseCase(hermes.device_discovery_service, hermes.device_transport_control_service)
    volume_set_request = VolumeSetRequestAdapter.from_intent_message(intentMessage)

    response = use_case.execute(volume_set_request)
    if not response:
        logging.info(response.value)
        hermes.publish_end_session(intentMessage.session_id, hermes.feedback_service.get_short_error_message())
    else:
        logging.info(response)
        hermes.publish_end_session(intentMessage.session_id, "")


@restore_volume_for_hotword
def mute_callback(hermes, intentMessage):
    use_case = MuteUseCase(hermes.device_discovery_service, hermes.device_transport_control_service)
    mute_request = MuteRequestAdapter.from_intent_message(intentMessage)

    response = use_case.execute(mute_request)
    if not response:
        logging.info(response.value)
        hermes.publish_end_session(intentMessage.session_id, hermes.feedback_service.get_short_error_message())
    else:
        logging.info(response)
        hermes.publish_end_session(intentMessage.session_id, "")


@restore_volume_for_hotword
def playTrack_callback(hermes, intentMessage):
    use_case = PlayTrackUseCase(hermes.device_discovery_service, hermes.music_search_service,
                                hermes.music_playback_service, hermes.feedback_service)
    play_track_request = PlayTrackRequestAdapter.from_intent_message(intentMessage)

    response = use_case.execute(play_track_request)

    if not response:
        logging.info(response.value)
        hermes.publish_end_session(intentMessage.session_id, hermes.feedback_service.get_short_error_message())
    else:
        logging.info(response)
        hermes.publish_end_session(intentMessage.session_id, "")


@restore_volume_for_hotword
def playArtist_callback(hermes, intentMessage):
    use_case = PlayArtistUseCase(hermes.device_discovery_service, hermes.music_search_service,
                                 hermes.music_playback_service, hermes.feedback_service)
    play_artist_request = PlayArtistRequestAdapter.from_intent_message(intentMessage)

    logging.info(play_artist_request)
    response = use_case.execute(play_artist_request)

    if not response:
        logging.info(response.value)
        hermes.publish_end_session(intentMessage.session_id, hermes.feedback_service.get_short_error_message())
    else:
        logging.info(response)
        hermes.publish_end_session(intentMessage.session_id, "")


@restore_volume_for_hotword
def playMusic_callback(hermes, intentMessage):
    use_case = PlayMusicUseCase(hermes.device_discovery_service, hermes.music_search_service,
                                hermes.music_playback_service, hermes.feedback_service)
    play_music_request = PlayMusicRequestAdapter.from_intent_message(intentMessage)

    response = use_case.execute(play_music_request)

    if not response:
        logging.error('Error type : {}'.format(response.type))
        logging.error('Error message : {}'.format(response.message))
        logging.error('Error exception : {}'.format(response.exception))
        logging.error(response.tb)

        feedback = hermes.feedback_service.from_response_object(response)
        hermes.publish_end_session(intentMessage.session_id, feedback)
    else:
        logging.debug("Response Success : {}".format(response))
        hermes.publish_end_session(intentMessage.session_id, response.feedback)


def get_playback_service(music_provider):
    if music_provider == "deezer":
        return DeezerNodeMusicPlaybackService()
    if music_provider == "spotify":
        return SpotifyNodeMusicPlaybackService(CONFIGURATION=CONFIGURATION)


def get_music_search_service(music_provider, device_disco_service):
    if music_provider == "spotify":
        return SpotifyMusicSearchService(CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN)
    if music_provider == "deezer":
        return DeezerMusicSearchService(device_disco_service)


if __name__ == "__main__":
    with Hermes(HERMES_HOST) as h:
        h.state_persistence_service = HermesStatePersistence(dict())
        h.device_discovery_service = NodeDeviceDiscoveryService(CONFIGURATION)
        h.device_transport_control_service = NodeDeviceTransportControlService(CONFIGURATION)
        h.feedback_service = FeedbackService(LANGUAGE)
        h.music_search_service = get_music_search_service(MUSIC_PROVIDER, h.device_discovery_service)
        h.music_playback_service = get_playback_service(MUSIC_PROVIDER)

        h \
            .subscribe_session_started(hotword_detected_callback) \
            .subscribe_intent("playMusic4", playMusic_callback) \
            .subscribe_intent("volumeUp4", volumeUp_callback) \
            .subscribe_intent("volumeDown4", volumeDown_callback) \
            .subscribe_intent("volumeSet4", volumeSet_callback) \
            .subscribe_intent("muteSound4", mute_callback) \
            .subscribe_intent("resumeMusic4", resumeMusic_callback) \
            .subscribe_intent("speakerInterrupt4", speakerInterrupt_callback) \
            .subscribe_intent("nextSong4", nextSong_callback) \
            .subscribe_intent("previousSong4", previousSong_callback) \
            .subscribe_intent("getInfos4", getInfos_callback) \
            .subscribe_session_ended(session_ended_callback) \
            .loop_forever()
