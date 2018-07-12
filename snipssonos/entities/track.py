from snipssonos.entities.entities import Entity


class Track(object):
    def __init__(self, uri, name=None, artists=None):
        self.uri = uri
        self.name = name
        self.artists = artists

    @classmethod
    def from_dict(cls, a_dict):
        name = None
        artists = None
        if 'name' in a_dict:
            name = a_dict['name']
        if 'artists' in a_dict:
            artists = a_dict['artists']
        track = cls(
            uri=a_dict['uri'],
            name=name,
            artists=artists
        )

        return track


Entity.register(Track)
