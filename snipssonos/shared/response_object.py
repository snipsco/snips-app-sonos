class ResponseSuccess(object):
    def __init__(self, value=None, feedback=None):
        self.value = value
        self.feedback = feedback

    def __nonzero__(self):
        return True


class ResponseFailure(object):
    RESOURCE_ERROR = 'ResourceError'
    PARAMETERS_ERROR = 'ParametersError'
    SYSTEM_ERROR = 'SystemError'

    def __init__(self, type_, message, exception=None, tb=None):
        self.type = type_
        self.message = self._format_message(message)
        self.exception = exception
        self.tb = tb

    def _format_message(self, str_or_exception):
        if isinstance(str_or_exception, Exception):
            return "{}: {}".format(str_or_exception.__class__.__name__, "{}".format(str_or_exception))
        return str_or_exception

    @property
    def value(self):
        return dict(
            type=self.type,
            message=self.message
        )

    def __nonzero__(self):
        return False

    @classmethod
    def build_from_invalid_request_object(cls, invalid_request_object):
        message = "\n".join(
            ["{}: {}".format(error['parameter'], error['message']) for error in invalid_request_object.errors])

        return cls(cls.PARAMETERS_ERROR, message)

    @classmethod
    def build_resource_error(cls, message, tb=None):
        return cls(cls.RESOURCE_ERROR, message, tb=tb)

    @classmethod
    def build_system_error(cls, message, exception, tb=None):
        return cls(cls.SYSTEM_ERROR, message, exception, tb)
