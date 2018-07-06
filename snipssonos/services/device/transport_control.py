class DeviceTransportControlService(object):  # TODO : Make this class abstract
    def pause(self, device):
        raise NotImplementedError("pause() is not implemented")

    def resume(self, device):
        raise NotImplementedError("resume() is not implemented")

    def volume_up(self, device):
        raise NotImplementedError("volume_up() is not implemented")

    def volume_down(self, device):
        raise NotImplementedError("volume_down() is not implemented")

    def set_volume(self, device):
        raise NotImplementedError("set_volume() is not implemented")

    def mute(self, device):
        raise NotImplementedError("mute() is not implemented")

    def next_track(self, device):
        raise NotImplementedError("next_track() is not implemented")

    def previous_track(self, device):
        raise NotImplementedError("previous_track() is not implemented")
