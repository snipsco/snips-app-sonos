from snipssonos.entities.entities import Entity


class Track(object):
    def __init__(self, uri, name=None):
        self.uri = uri
        self.name = name

    @classmethod
    def from_dict(cls, a_dict):
        name = None
        if 'name' in a_dict:
            name = a_dict['name']
        track = cls(
            uri=a_dict['uri'],
            name=name
        )

        return track


Entity.register(Track)
