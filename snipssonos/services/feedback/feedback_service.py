from __future__ import unicode_literals

from snipssonos.services.feedback.feedback_messages import *
import snipssonos.exceptions


class FeedbackService:
    FEEDBACK_OBJECT = {
        'en': {
            'generic_error': EN_TTS_GENERIC_ERROR,
            'short_error': EN_TTS_SHORT_ERROR,
            'no_tracks_error': EN_TTS_TRACK_INFO_NO_TRACKS_ERROR,
            'device_discovery': EN_TTS_DEVICE_DISCOVERY_SERVICE_UNREACHABLE,
            'playlist': EN_TTS_PLAYING_PLAYLIST_TEMPLATE,
            'track': EN_TTS_PLAYING_TRACK_TEMPLATE,
            'album': EN_TTS_PLAYING_ALBUM_TEMPLATE,
            'album_short': EN_TTS_PLAYING_ALBUM_SHORT_TEMPLATE,
            'artist': EN_TTS_PLAYING_ARTIST_TEMPLATE,
            'track_info': EN_TTS_TRACK_INFO
        },
        'fr': {
            'generic_error': FR_TTS_GENERIC_ERROR,
            'short_error': FR_TTS_SHORT_ERROR,
            'no_tracks_error': FR_TTS_TRACK_INFO_NO_TRACKS_ERROR,
            'device_discovery': FR_TTS_DEVICE_DISCOVERY_SERVICE_UNREACHABLE,
            'playlist': FR_TTS_PLAYING_PLAYLIST_TEMPLATE,
            'track': FR_TTS_PLAYING_TRACK_TEMPLATE,
            'album': FR_TTS_PLAYING_ALBUM_TEMPLATE,
            'album_short': FR_TTS_PLAYING_ALBUM_SHORT_TEMPLATE,
            'artist': FR_TTS_PLAYING_ARTIST_TEMPLATE,
            'track_info': FR_TTS_TRACK_INFO
        }
    }

    SUPPORTED_LANGUAGES = ['en', 'fr']

    def __init__(self, language):
        self.validate_language(language)
        self.language = language

    def set_language(self, language):
        self.validate_language(language)
        self.language = language

    def get_generic_error_message(self):
        return self.FEEDBACK_OBJECT[self.language]['generic_error']

    def get_short_error_message(self):
        return self.FEEDBACK_OBJECT[self.language]['short_error']

    def get_device_discovery_message(self):
        return self.FEEDBACK_OBJECT[self.language]['device_discovery']

    def get_playlist_template(self):
        return self.FEEDBACK_OBJECT[self.language]['playlist']

    def get_track_template(self):
        return self.FEEDBACK_OBJECT[self.language]['track']

    def get_album_template(self):
        return self.FEEDBACK_OBJECT[self.language]['album']

    def get_album_short_template(self):
        return self.FEEDBACK_OBJECT[self.language]['album_short']

    def get_artist_template(self):
        return self.FEEDBACK_OBJECT[self.language]['artist']

    def get_track_info_template(self):
        return self.FEEDBACK_OBJECT[self.language]['track_info']

    def get_no_tracks_error_message(self):
        return self.FEEDBACK_OBJECT[self.language]['no_tracks_error']

    def concatenate_artists_in_string(self, artists):
        # if more than one artist is found we concatenate them in a string
        artist_names = [artist.name for artist in artists]
        return ", ".join(artist_names).strip()

    def validate_language(self, language):
        if not (language in self.SUPPORTED_LANGUAGES):
            class_name = self.__class__.__name__
            raise AttributeError(
                "Tried to assign an unsupported language to the language property of {}".format(class_name))
        return True

    def from_response_object(self, response_object):
        if response_object:  # ResponseSuccess
            return response_object.feedback
        else:  # ResponseFailure
            # TODO : Complete this by mapping specific exceptions to the correct TTS sentences.
            if response_object.type == "ResourceError":
                return response_object.message

            if isinstance(response_object.exception, snipssonos.exceptions.DeviceDiscoveryException):
                return self.get_device_discovery_message()

            if isinstance(response_object.exception, snipssonos.exceptions.SonosActionException):
                return self.get_generic_error_message()

            return self.get_short_error_message()

    def get_album_message(self, album_name, artist_name=None):
        if not(artist_name is None):
            return self.get_album_template().format(album_name, artist_name)
        return self.get_album_short_template().format(album_name)


