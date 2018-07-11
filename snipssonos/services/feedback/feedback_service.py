from snipssonos.shared.feedback import *


class FeedbackService:
    FEEDBACK_MESSAGES = {
        'en': {
            'generic_error': EN_TTS_GENERIC_ERROR,
            'short_error': EN_TTS_SHORT_ERROR,
            'device_discovery': EN_TTS_DEVICE_DISCOVERY_SERVICE_UNREACHABLE,
            'playlist': EN_TTS_PLAYING_PLAYLIST_TEMPLATE,
            'track': EN_TTS_PLAYING_TRACK_TEMPLATE,
            'album': EN_TTS_ALBUM_ALBUM_TEMPLATE,
            'artist': EN_TTS_PLAYING_ARTIST_TEMPLATE
        },
        'fr': {
            'generic_error': FR_TTS_GENERIC_ERROR,
            'short_error': FR_TTS_SHORT_ERROR,
            'device_discovery': FR_TTS_DEVICE_DISCOVERY_SERVICE_UNREACHABLE,
            'playlist': FR_TTS_PLAYING_PLAYLIST_TEMPLATE,
            'track': FR_TTS_PLAYING_TRACK_TEMPLATE,
            'album': FR_TTS_ALBUM_TEMPLATE,
            'artist': FR_TTS_PLAYING_ARTIST_TEMPLATE
        }
    }

    AVAILABLE_LANGUAGES = ['en', 'fr']

    def __init__(self):
        self.language = None
        pass

    def set_language(self, language):
        self.validate_language(language)
        self.language = language

    def get_generic_error_message(self):
        return self.FEEDBACK_MESSAGES[self.language]['generic_error']

    def get_short_error_message(self):
        return self.FEEDBACK_MESSAGES[self.language]['short_error']

    def get_device_discovery_message(self):
        return self.FEEDBACK_MESSAGES[self.language]['device_discovery']

    def get_playlist_template(self):
        return self.FEEDBACK_MESSAGES[self.language]['playlist']

    def get_track_template(self):
        return self.FEEDBACK_MESSAGES[self.language]['track']

    def get_album_template(self):
        return self.FEEDBACK_MESSAGES[self.language]['album']

    def get_artist_template(self):
        return self.FEEDBACK_MESSAGES[self.language]['artist']

    def validate_language(self, language):
        return language in self.AVAILABLE_LANGUAGES


