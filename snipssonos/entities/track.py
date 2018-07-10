from snipssonos.entities.entities import Entity


class Track(object):
    def __init__(self, uri, name=None, artist_name=None):
        self.uri = uri
        self.name = name
        self.artist_name = artist_name

    @classmethod
    def from_dict(cls, a_dict):
        name = None
        artist_name = None
        if 'name' in a_dict:
            name = a_dict['name']
        if 'artist_name' in a_dict:
            artist_name = a_dict['artist_name']
        track = cls(
            uri=a_dict['uri'],
            name=name,
            artist_name=artist_name
        )

        return track


Entity.register(Track)
