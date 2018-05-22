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


class VolumeUpRequestObject(object):
    def __init__(self,  volume_increase=None):
        self.volume_increase = volume_increase

    def __nonzero__(self):
        return True

    @classmethod
    def from_dict(cls, d):
        invalid_request = InvalidRequestObject()

        if 'volume_increase' in d and not isinstance(d['volume_increase'], int):
            invalid_request.add_error('volume_increase', 'must be an integer')

        if 'volume_increase' in d and isinstance(d['volume_increase'], int) and d['volume_increase'] < 0:
            invalid_request.add_error('volume_increase', 'must be positive')

        if 'volume_increase' in d and isinstance(d['volume_increase'], int) and d['volume_increase'] > 100:
            invalid_request.add_error('volume_increase', 'must be lower than 100')

        if invalid_request.has_errors():
            return invalid_request

        return cls(
            volume_increase=d.get('volume_increase', None)
        )