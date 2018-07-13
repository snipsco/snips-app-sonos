from snipssonos.entities.entities import Entity


class Album(object):
    def __init__(self, uri, name, artists=None):
        self.uri = uri
        self.name = name
        self.artists = artists

    @classmethod
    def from_dict(cls, a_dict):
        album = cls(
            uri=a_dict['uri'],
            name=a_dict['name'],
            artists=a_dict['artists']
        )

        return album


Entity.register(Album)
