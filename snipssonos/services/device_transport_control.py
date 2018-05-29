class DeviceTransportControlService(object): # TODO : Make this class abstract
    def volume_up(self, device):
        raise NotImplementedError("volume_up() is not implemented")

    def volume_down(self, device):
        raise NotImplementedError("volume_down() is not implemented")