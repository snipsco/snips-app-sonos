from snipssonos.entities.entities import Entity


class Track(object):
    def __init__(self, uri):
        self.uri = uri

    @classmethod
    def from_dict(cls, a_dict):
        track = cls(
            uri=a_dict['uri']
        )

        return track


Entity.register(Track)
