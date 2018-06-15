from snipssonos.entities.entities import Entity


class Playlist(object):
    def __init__(self, uri, name):
        self.uri = uri
        self.name = name

    @classmethod
    def from_dict(cls, a_dict):
        playlist = cls(
            uri=a_dict['uri'],
            name=a_dict['name']
        )

        return playlist


Entity.register(Playlist)
