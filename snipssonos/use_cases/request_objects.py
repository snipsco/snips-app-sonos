class InvalidRequestObject(object):
    def __init__(self):
        self.errors = list()

    def add_error(self, parameter, value):
        self.errors.append({'parameter': parameter, 'message': value})

class VolumeUpRequestObject(object):

    def __nonzero__(self):
        return True

    @classmethod
    def from_dict(cls, d):
        return cls()

