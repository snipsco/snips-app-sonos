from snipssonos.services.feedback.feedback_messages import *
import snipssonos.exceptions
import snipssonos.shared.response_object as reso
from snipssonos.shared.error import Volume, OutOfRangeError


class FeedbackService(object):
    FEEDBACK_OBJECT = {
        'en': {
            'generic_error': EN_TTS_GENERIC_ERROR,
            'short_error': EN_TTS_SHORT_ERROR,
            'no_tracks_error': EN_TTS_TRACK_INFO_NO_TRACKS_ERROR,
            'device_discovery': EN_TTS_DEVICE_DISCOVERY_SERVICE_UNREACHABLE,
            'playlist': EN_TTS_PLAYING_PLAYLIST_TEMPLATE,
            'track': EN_TTS_PLAYING_TRACK_TEMPLATE,
            'album': EN_TTS_PLAYING_ALBUM_TEMPLATE,
            'artist': EN_TTS_PLAYING_ARTIST_TEMPLATE,
            'track_info': EN_TTS_TRACK_INFO,
            'parameters_error': EN_TTS_PARAMETERS_ERROR,
            'parameters_error_out_of_range': EN_TTS_PARAMETERS_ERROR_OUT_OF_RANGE,
            'parameters_error_missing': EN_TTS_PARAMETERS_ERROR_MISSING
        },
        'fr': {
            'generic_error': FR_TTS_GENERIC_ERROR,
            'short_error': FR_TTS_SHORT_ERROR,
            'no_tracks_error': FR_TTS_TRACK_INFO_NO_TRACKS_ERROR,
            'device_discovery': FR_TTS_DEVICE_DISCOVERY_SERVICE_UNREACHABLE,
            'playlist': FR_TTS_PLAYING_PLAYLIST_TEMPLATE,
            'track': FR_TTS_PLAYING_TRACK_TEMPLATE,
            'album': FR_TTS_PLAYING_ALBUM_TEMPLATE,
            'artist': FR_TTS_PLAYING_ARTIST_TEMPLATE,
            'track_info': FR_TTS_TRACK_INFO,
            'parameters_error': FR_TTS_PARAMETERS_ERROR,
            'parameters_error_out_of_range': FR_TTS_PARAMETERS_ERROR_OUT_OF_RANGE,
            'parameters_error_missing': FR_TTS_PARAMETERS_ERROR_MISSING
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

    def get_no_tracks_error_message(self):
        return self.FEEDBACK_OBJECT[self.language]['no_tracks_error']

    def get_parameter_error_message(self, error):
        if error['type'] == "WRONG_TYPE":
            return self.FEEDBACK_OBJECT[self.language]['parameters_error'].format(error['parameter'])
        if error['type'] == "OUT_OF_RANGE":
            return self.FEEDBACK_OBJECT[self.language]['parameters_error_out_of_range'].format(error['parameter'], 0, 100)
        if error['type'] == "MISSING":
            return self.FEEDBACK_OBJECT[self.language]['parameters_error_missing'].format(error['parameter'])

        return self.FEEDBACK_OBJECT[self.language]['parameters_error'].format(error['parameter'])


    def get_playlist_template(self):
        return self.FEEDBACK_OBJECT[self.language]['playlist']

    def get_track_template(self):
        return self.FEEDBACK_OBJECT[self.language]['track']

    def get_album_template(self):
        return self.FEEDBACK_OBJECT[self.language]['album']

    def get_artist_template(self):
        return self.FEEDBACK_OBJECT[self.language]['artist']

    def get_track_info_template(self):
        return self.FEEDBACK_OBJECT[self.language]['track_info']

    def get_parameters_error_template(self):
        return self.FEEDBACK_OBJECT[self.language]['parameters_error']

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


    def get_feedback_from_error(self, error):
        if isinstance(error, OutOfRangeError):
            param_desc = error.parameter.get_description(self.language)
            return self.FEEDBACK_OBJECT[self.language]['parameters_error_out_of_range'].format(param_desc)

        return self.get_short_error_message()

    def from_response_object(self, response_object):
        if response_object:  # ResponseSuccess
            return response_object.feedback
        else:  # ResponseFailure
            if reso.ResponseFailure.PARAMETERS_ERROR == response_object.type:
                feedback = ".\n".join([self.get_feedback_from_error(error) for error in response_object.errors])
                return feedback

            if reso.ResponseFailure.SYSTEM_ERROR == response_object.type:
                return EMPTY_SENTENCE

            if reso.ResponseFailure.RESOURCE_ERROR == response_object.type:
                return EMPTY_SENTENCE

            return self.get_short_error_message()



