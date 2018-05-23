from snipssonos.entities.entities import Entity

class Device(object):
    def __init__(self, identifier, name, volume):
        self.name = name
        self.identifier = identifier
        self.volume = volume

    @classmethod
    def from_dict(cls, a_dictionary):
        device = cls(
            name= a_dictionary['name'],
            identifier=a_dictionary['identifier'],
            volume=a_dictionary['volume']
        )
        return device


Entity.register(Device)
