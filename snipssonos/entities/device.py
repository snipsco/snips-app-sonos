from snipssonos.entities.entities import Entity

class Device(object):
    def __init__(self, identifier, name):
        self.name = name
        self.identifier = identifier

    @classmethod
    def from_dict(cls, dictio):
        device = cls(
            name= dictio['name'],
            identifier=dictio['identifier']
        )
        return device


Entity.register(Device)
