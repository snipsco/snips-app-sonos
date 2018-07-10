from snipssonos.entities.entities import Entity


class Album(object):
    def __init__(self, uri, name, artist_name=None):
        self.uri = uri
        self.name = name
        self.artist_name = artist_name

    @classmethod
    def from_dict(cls, a_dict):
        album = cls(
            uri=a_dict['uri'],
            name=a_dict['name'],
            artist_name=a_dict['artist_name']
        )

        return album


Entity.register(Album)
