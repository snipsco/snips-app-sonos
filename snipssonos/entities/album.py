from snipssonos.entities.entities import Entity

class Album(object):
    def __init__(self, uri, name):
        self.uri = uri
        self.name = name

    @classmethod
    def from_dict(cls, a_dict):
        album = cls(
            uri=a_dict['uri'],
            name=a_dict['name']
        )

        return album


Entity.register(Album)
