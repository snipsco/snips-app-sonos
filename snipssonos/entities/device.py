from snipssonos.entities.entities import Entity

class Device(object):
    def __init__(self, identifier, name):
        self.name = name
        self.identifier = identifier

    @classmethod
    def from_dict(cls, a_dictionary):
        device = cls(
            name= a_dictionary['name'],
            identifier=a_dictionary['identifier']
        )
        return device


Entity.register(Device)
