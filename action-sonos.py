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
from snipssonos.use_cases.play.playlist import PlayPlaylistUseCase
from snipssonos.use_cases.play.album import PlayAlbumUseCase
from snipssonos.use_cases.resume_music import ResumeMusicUseCase
from snipssonos.use_cases.speaker_interrupt import SpeakerInterruptUseCase
from snipssonos.use_cases.next_track import NextTrackUseCase

from snipssonos.adapters.request_adapter import VolumeUpRequestAdapter, PlayTrackRequestAdapter, \
    PlayArtistRequestAdapter, VolumeSetRequestAdapter, VolumeDownRequestAdapter, ResumeMusicRequestAdapter, \
    SpeakerInterruptRequestAdapter, MuteRequestAdapter, PlayPlaylistRequestAdapter, PlayAlbumRequestAdapter, \
    PlayMusicRequestAdapter, NextTrackRequestAdapter
from snipssonos.services.node.device_discovery_service import NodeDeviceDiscoveryService
from snipssonos.services.node.device_transport_control import NodeDeviceTransportControlService
from snipssonos.services.node.music_playback_service import NodeMusicPlaybackService
from snipssonos.services.spotify.music_search_service import SpotifyMusicSearchService

from snipssonos.shared.feedback import FR_TTS_SHORT_ERROR

# Utils functions
CONFIG_INI = "config.ini"

HOSTNAME = "localhost"

HERMES_HOST = "{}:1883".format(HOSTNAME)
MOPIDY_HOST = HOSTNAME

# Logging config
logging.basicConfig(level=logging.INFO)

# Music management functions

def addSong_callback(hermes, intentMessage):
    raise NotImplementedError("addSong_callback() not implemented")


def getInfos_callback(hermes, intentMessage):
    raise NotImplementedError("getInfos_callback() not implemented")


def playAlbum_callback(hermes, intentMessage):
    use_case = PlayAlbumUseCase(hermes.device_discovery_service, hermes.music_search_service,
                                hermes.music_playback_service)
    play_album_request = PlayAlbumRequestAdapter.from_intent_message(intentMessage)

    logging.info(play_album_request)
    response = use_case.execute(play_album_request)

    if not response:
        logging.info(response)
        hermes.publish_end_session(intentMessage.session_id, response.message)
    else:
        logging.info(response)
        hermes.publish_end_session(intentMessage.session_id, response.feedback)


def playPlaylist_callback(hermes, intentMessage):
    use_case = PlayPlaylistUseCase(hermes.device_discovery_service, hermes.music_search_service,
                                   hermes.music_playback_service)
    play_playlist_request = PlayPlaylistRequestAdapter.from_intent_message(intentMessage)

    logging.info(play_playlist_request)
    response = use_case.execute(play_playlist_request)

    if not response:
        logging.info(response)
        hermes.publish_end_session(intentMessage.session_id, response.message)
    else:
        logging.info(response)
        hermes.publish_end_session(intentMessage.session_id, response.feedback)


def radioOn_callback(hermes, intentMessage):
    raise NotImplementedError("radioOn_callback() not implemented")


def previousSong_callback(hermes, intentMessage):
    raise NotImplementedError("previousSong_callback() not implemented")


def nextSong_callback(hermes, intentMessage):
    usecase = NextTrackUseCase(hermes.device_discovery_service, hermes.device_transport_control_service)

    next_track_request = NextTrackRequestAdapter.from_intent_message(intentMessage)

    response = usecase.execute(next_track_request)
    if not response:
        logging.info(response.value)
        hermes.publish_end_session(intentMessage.session_id, FR_TTS_SHORT_ERROR)
    else:
        logging.info(response)
        hermes.publish_end_session(intentMessage.session_id, "")



def resumeMusic_callback(hermes, intentMessage):  # Playback functions
    usecase = ResumeMusicUseCase(hermes.device_discovery_service, hermes.device_transport_control_service)
    resume_music_request = ResumeMusicRequestAdapter.from_intent_message(intentMessage)

    response = usecase.execute(resume_music_request)
    if not response:
        logging.info(response.value)
        hermes.publish_end_session(intentMessage.session_id, FR_TTS_SHORT_ERROR)
    else:
        logging.info(response)
        hermes.publish_end_session(intentMessage.session_id, "")


def speakerInterrupt_callback(hermes, intentMessage):
    usecase = SpeakerInterruptUseCase(hermes.device_discovery_service, hermes.device_transport_control_service)
    speaker_interrupt_request = SpeakerInterruptRequestAdapter.from_intent_message(intentMessage)

    response = usecase.execute(speaker_interrupt_request)
    if not response:
        logging.info(response.value)
        hermes.publish_end_session(intentMessage.session_id, FR_TTS_SHORT_ERROR)
    else:
        logging.info(response)
        hermes.publish_end_session(intentMessage.session_id, "")


def volumeDown_callback(hermes, intentMessage):
    usecase = VolumeDownUseCase(hermes.device_discovery_service, hermes.device_transport_control_service)
    volume_down_request = VolumeDownRequestAdapter.from_intent_message(intentMessage)

    response = usecase.execute(volume_down_request)
    if not response:
        logging.info(response.value)
        hermes.publish_end_session(intentMessage.session_id, FR_TTS_SHORT_ERROR)
    else:
        logging.info(response)
        hermes.publish_end_session(intentMessage.session_id, "")


def volumeUp_callback(hermes, intentMessage):
    usecase = VolumeUpUseCase(hermes.device_discovery_service, hermes.device_transport_control_service)
    volume_up_request = VolumeUpRequestAdapter.from_intent_message(intentMessage)

    response = usecase.execute(volume_up_request)
    if not response:
        logging.info(response.value)
        hermes.publish_end_session(intentMessage.session_id, FR_TTS_SHORT_ERROR)
    else:
        logging.info(response)
        hermes.publish_end_session(intentMessage.session_id, "")


def volumeSet_callback(hermes, intentMessage):
    usecase = VolumeSetUseCase(hermes.device_discovery_service, hermes.device_transport_control_service)
    volume_set_request = VolumeSetRequestAdapter.from_intent_message(intentMessage)

    response = usecase.execute(volume_set_request)
    if not response:
        logging.info(response.value)
        hermes.publish_end_session(intentMessage.session_id, FR_TTS_SHORT_ERROR)
    else:
        logging.info(response)
        hermes.publish_end_session(intentMessage.session_id, "")


def mute_callback(hermes, intentMessage):
    usecase = MuteUseCase(hermes.device_discovery_service, hermes.device_transport_control_service)
    mute_request = MuteRequestAdapter.from_intent_message(intentMessage)

    response = usecase.execute(mute_request)
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


    logging.info(play_music_request)
    response = use_case.execute(play_music_request)

    if not response:
        hermes.publish_end_session(intentMessage.session_id, FR_TTS_SHORT_ERROR)
    else:
        hermes.publish_end_session(intentMessage.session_id, response.feedback)

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
            .subscribe_intent("playMusic4", playMusic_callback) \
            .subscribe_intent("volumeUp4", volumeUp_callback) \
            .subscribe_intent("volumeDown4", volumeDown_callback) \
            .subscribe_intent("volumeSet4", volumeSet_callback) \
            .subscribe_intent("muteSound4", mute_callback) \
            .subscribe_intent("resumeMusic4", resumeMusic_callback) \
            .subscribe_intent("speakerInterrupt4", speakerInterrupt_callback) \
            .subscribe_intent("nextSong4", nextSong_callback) \
            .loop_forever()
