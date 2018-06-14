from snipssonos.entities.entities import Entity

class Artist(object):
    def __init__(self, uri, name):
        self.uri = uri
        self.name = name

    @classmethod
    def from_dict(cls, a_dict):
        artist = cls(
            uri=a_dict['uri'],
            name=a_dict['name']
        )

        return artist


Entity.register(Artist)
