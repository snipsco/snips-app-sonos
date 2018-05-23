from snipssonos.entities.entities import Entity

class Device(object):
    VOLUME_MAX = 100
    VOLUME_MIN = 0

    def __init__(self, identifier, name, volume):
        self.name = name
        self.identifier = identifier
        self._volume = volume

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value):
        if value < self.VOLUME_MIN:
            self._volume = self.VOLUME_MIN
        elif value > self.VOLUME_MAX:
            self._volume = self.VOLUME_MAX
        else:
            self._volume = value


    @classmethod
    def from_dict(cls, a_dictionary):
        device = cls(
            name= a_dictionary['name'],
            identifier=a_dictionary['identifier'],
            volume=a_dictionary['volume']
        )
        return device

    def increase_volume(self, volume_increment):
        self.volume = self.volume + volume_increment


Entity.register(Device)
