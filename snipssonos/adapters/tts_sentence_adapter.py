from snipssonos.shared import feedback
import snipssonos.exceptions


class TTSSentenceGenerator(object):
    SUPPORTED_LANGUAGES = ["FRENCH", "ENGLISH"]

    def __init__(self, lang):
        self.language = lang

    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, lang):
        if not (lang in self.SUPPORTED_LANGUAGES):
            class_name = self.__class__.__name__
            raise AttributeError(
                "Tried to assign an unsupported language to the language property of {}".format(class_name))
        else:
            self._language = lang

    def from_response_object(self, response_object):
        if response_object: # ResponseSuccess
            return response_object.message
        else: # ResponseFailure
            if response_object.type == "ResourceError":
                return response_object.message
            # TODO : Complete this by mapping specific exceptions to the correct TTS sentences.
            if isinstance(response_object.exception, snipssonos.exceptions.SonosActionException):
                return feedback.FR_TTS_GENERIC_ERROR

            if isinstance(response_object.exception, snipssonos.exceptions.DeviceDiscoveryException):
                return feedback.FR_TTS_DEVICE_DISCOVERY_SERVICE_UNREACHABLE

            else:
                return feedback.FR_TTS_SHORT_ERROR
