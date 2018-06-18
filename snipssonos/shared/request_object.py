from snipssonos.exceptions import RequestObjectInitializationException

class InvalidRequestObject(object):
    def __init__(self):
        self.errors = list()

    def __nonzero__(self):
        return False

    __bool__ = __nonzero__

    def add_error(self, parameter, value):
        self.errors.append({'parameter': parameter, 'message': value})

    def has_errors(self):
        return bool(len(self.errors))


class ValidRequestObject(object):
    def __nonzero__(self):
        return True

    __bool__ = __nonzero__

    @classmethod
    def from_dict(cls, adict):
        raise NotImplementedError


class RequestObjectFactory(object):
    request_object_class = ValidRequestObject

    @classmethod
    def from_dict(cls, a_dict):
        try:
            return cls.request_object_class.from_dict(a_dict)
        except RequestObjectInitializationException as exception:
            return exception.invalid_request_object