from snipssonos.services.feedback.feedback_messages import *
import snipssonos.exceptions


class FeedbackService:
    FEEDBACK_OBJECT = {
        'en': {
            'generic_error': EN_TTS_GENERIC_ERROR,
            'short_error': EN_TTS_SHORT_ERROR,
            'device_discovery': EN_TTS_DEVICE_DISCOVERY_SERVICE_UNREACHABLE,
            'playlist': EN_TTS_PLAYING_PLAYLIST_TEMPLATE,
            'track': EN_TTS_PLAYING_TRACK_TEMPLATE,
            'album': EN_TTS_PLAYING_ALBUM_TEMPLATE,
            'artist': EN_TTS_PLAYING_ARTIST_TEMPLATE
        },
        'fr': {
            'generic_error': FR_TTS_GENERIC_ERROR,
            'short_error': FR_TTS_SHORT_ERROR,
            'device_discovery': FR_TTS_DEVICE_DISCOVERY_SERVICE_UNREACHABLE,
            'playlist': FR_TTS_PLAYING_PLAYLIST_TEMPLATE,
            'track': FR_TTS_PLAYING_TRACK_TEMPLATE,
            'album': FR_TTS_PLAYING_ALBUM_TEMPLATE,
            'artist': FR_TTS_PLAYING_ARTIST_TEMPLATE
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

    def get_artist_template(self):
        return self.FEEDBACK_OBJECT[self.language]['artist']

    def validate_language(self, language):
        if not (language in self.SUPPORTED_LANGUAGES):
            class_name = self.__class__.__name__
            raise AttributeError(
                "Tried to assign an unsupported language to the language property of {}".format(class_name))
        return True

    def from_response_object(self, response_object):
        if response_object:  # ResponseSuccess
            return response_object.feedback
        else: # ResponseFailure
            # TODO : Complete this by mapping specific exceptions to the correct TTS sentences.
            if isinstance(response_object.exception, snipssonos.exceptions.SonosActionException):
                return self.get_generic_error_message()

            if isinstance(response_object.exception, snipssonos.exceptions.DeviceDiscoveryException):
                return self.get_device_discovery_message()

            return self.get_short_error_message()


