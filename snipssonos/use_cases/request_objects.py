class InvalidRequestObject(object):

    def __nonzero__(self):
        return False

    __bool__ = __nonzero__

    def __init__(self):
        self.errors = list()

    def add_error(self, parameter, value):
        self.errors.append({'parameter': parameter, 'message': value})

    def has_errors(self):
        return bool(len(self.errors))

class VolumeUpRequestObject(object):

    def __init__(self,  volume_increase_in_percent=None):
        self.volume_increase_in_percent = volume_increase_in_percent

    def __nonzero__(self):
        return True

    @classmethod
    def from_dict(cls, d):
        invalid_request = InvalidRequestObject()

        if 'volume_increase_in_percent' in d and not isinstance(d['volume_increase_in_percent'], int):
            invalid_request.add_error('volume_increase_in_percent', 'must be an integer')



        if invalid_request.has_errors():
            return invalid_request

        return cls(
            volume_increase_in_percent=d.get('volume_increase_in_percent', None)
        )